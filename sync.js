// 教科書の記録を、ID とパスワードでログインした Firebase（Firestore）に置いて、スマホと PC で合わせる。
// ID とパスワードが同じなら同じ人。Firebase の中では ID を「ID@textbooks.example.com」の形のメールアドレスとして使う（メールは送らない）。
// firebase-config.js が null のあいだは何もしない（記録は端末の中だけ）。
//
// しくみ
// - 記録は今までどおり localStorage（textbooks-…）。index.html の store.set が、変わったキーを window.tbChanged に積む
// - ログインしていれば、変わったキーを 8秒ごと（とページを離れるとき）に users/{uid}/kv/{キー} へ書く。中身は { v: 文字列, t: 変えた時刻, dev: 端末 }
// - ほかの端末が書いたものは onSnapshot で受け取り、新しいほう（t が大きいほう）を使う
// - 勉強時間（textbooks-study）だけは端末ごとに study-dev-{端末} に置き、ほかの端末の分を textbooks-study-others に入れて足し合わせる
// - 同期を始める前から両方にあった記録は、最初の1回だけ合わせる（付箋・練習問題・単語のチェック・今勉強中の並び）
import config from "./firebase-config.js";

const CDN = "https://www.gstatic.com/firebasejs/10.12.2/";
const ls = {
  get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
};
const META = "textbooks-sync-meta", DEV = "textbooks-device", OTHERS = "textbooks-study-others";
const LOCAL_ONLY = new Set([META, DEV, OTHERS]);
const syncable = (k) => typeof k === "string" && k.startsWith("textbooks-") && !LOCAL_ONLY.has(k);
const parse = (s, d) => { try { const v = JSON.parse(s); return v == null ? d : v; } catch (e) { return d; } };
const dev = ls.get(DEV) || (() => { const d = Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4); ls.set(DEV, d); return d; })();
const STUDY_DOC = "study-dev-" + dev;
const docIdOf = (k) => (k === "textbooks-study" ? STUDY_DOC : k);
const meta = parse(ls.get(META), {});
const saveMeta = () => ls.set(META, JSON.stringify(meta));
const dirty = new Set();
let user = null, flushTimer = 0, refreshTimer = 0, F = null, db = null;

if (!config) window.tbChanged = { push() {} };   // 設定がないあいだは、積まない
if (config) {
  // index.html が積んでおいた「変わったキー」を受け取り、これからはすぐ受け取る
  const take = ([k, t]) => { if (!syncable(k)) return; meta[k] = t || Date.now(); dirty.add(k); };
  (Array.isArray(window.tbChanged) ? window.tbChanged : []).forEach(take);
  window.tbChanged = { push(x) { take(x); saveMeta(); schedule(); } };
  saveMeta();
  start().catch((e) => { console.warn("sync:", e); status("err"); });
}

function schedule() { clearTimeout(flushTimer); flushTimer = setTimeout(flush, 8000); }
function refresh() { clearTimeout(refreshTimer); refreshTimer = setTimeout(() => window.tbRefresh && window.tbRefresh(), 300); }

async function start() {
  const [{ initializeApp }, A, Fs] = await Promise.all([
    import(CDN + "firebase-app.js"), import(CDN + "firebase-auth.js"), import(CDN + "firebase-firestore.js"),
  ]);
  F = Fs;
  const app = initializeApp(config), auth = A.getAuth(app);
  db = F.getFirestore(app);
  let unsub = null;
  ui.login = (id, pw, isNew) => (isNew ? A.createUserWithEmailAndPassword : A.signInWithEmailAndPassword)(auth, id + ID_DOMAIN, pw);
  ui.logout = async () => { await flush(); await A.signOut(auth); };
  A.onAuthStateChanged(auth, async (u) => {
    if (unsub) { unsub(); unsub = null; }
    user = u;
    ready = true;
    status(u ? "sync" : "");
    if (!u) return;
    try {
      await firstSync();
      unsub = F.onSnapshot(F.collection(db, "users", u.uid, "kv"), onSnap, () => status("err"));
      status("ok");
    } catch (e) { console.warn("sync:", e); status("err"); }
  });
  addEventListener("visibilitychange", () => { if (document.hidden) flush(); });
  addEventListener("pagehide", () => flush());
}

// 同期を始める前から両方にあった記録の合わせ方（それ以外は、ほかの端末の記録を使う）
function mergeFirst(k, local, remote) {
  const a = parse(local, null), b = parse(remote, null);
  if (k === "textbooks-notes" && Array.isArray(a) && Array.isArray(b)) {
    const seen = new Set(b.map((x) => x && x.id));
    return JSON.stringify(b.concat(a.filter((x) => x && !seen.has(x.id))));
  }
  if ((k === "textbooks-studying" || /^textbooks-words-(?!view-|hide)/.test(k)) && Array.isArray(a) && Array.isArray(b)) {
    return JSON.stringify(b.concat(a.filter((x) => !b.includes(x))));
  }
  if (/^textbooks-quiz(log)?-/.test(k) && a && b && typeof a === "object" && typeof b === "object" && !Array.isArray(a)) {
    return JSON.stringify({ ...b, ...a });
  }
  return remote;
}

async function firstSync() {
  const snap = await F.getDocs(F.collection(db, "users", user.uid, "kv"));
  const remote = {}, others = {};
  let changed = false;
  snap.forEach((d) => { remote[d.id] = d.data(); });
  for (const [id, d] of Object.entries(remote)) {
    if (id.startsWith("study-dev-")) { if (id !== STUDY_DOC) others[id.slice(10)] = parse(d.v, {}); continue; }
    if (!syncable(id)) continue;
    const local = ls.get(id), lt = meta[id] || 0;
    if (local === d.v) { meta[id] = Math.max(lt, d.t); continue; }
    if (local !== null && !lt) {              // この端末に前からあった記録と、ほかの端末の記録を合わせる
      ls.set(id, mergeFirst(id, local, d.v)); meta[id] = Date.now(); dirty.add(id); changed = true;
    } else if (d.t > lt) {
      ls.set(id, d.v); meta[id] = d.t; dirty.delete(id); changed = true;
    }
  }
  if (remote[STUDY_DOC] && ls.get("textbooks-study") === null) { ls.set("textbooks-study", remote[STUDY_DOC].v); changed = true; }
  ls.set(OTHERS, JSON.stringify(others));
  // この端末にしかない記録・この端末のほうが新しい記録を送る
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i);
    if (!syncable(k)) continue;
    const r = remote[docIdOf(k)];
    if (!r || r.v !== ls.get(k) && (k === "textbooks-study" || (meta[k] || 0) > r.t)) dirty.add(k);
  }
  saveMeta();
  await flush();
  if (changed || Object.keys(others).length) refresh();
}

function onSnap(qs) {
  let changed = false;
  qs.docChanges().forEach((ch) => {
    if (ch.type === "removed") return;
    const id = ch.doc.id, d = ch.doc.data();
    if (d.dev === dev) return;                 // この端末が書いたもの
    if (id.startsWith("study-dev-")) {
      const o = parse(ls.get(OTHERS), {});
      o[id.slice(10)] = parse(d.v, {});
      ls.set(OTHERS, JSON.stringify(o));
      changed = true;
      return;
    }
    if (!syncable(id) || (meta[id] || 0) >= d.t) return;
    ls.set(id, d.v); meta[id] = d.t; dirty.delete(id); changed = true;
  });
  if (changed) { saveMeta(); refresh(); }
}

async function flush() {
  clearTimeout(flushTimer);
  if (!user || !db || !dirty.size) return;
  const keys = [...dirty];
  dirty.clear();
  const batch = F.writeBatch(db);
  keys.forEach((k) => {
    const v = ls.get(k);
    if (v === null) return;
    if (!meta[k]) meta[k] = Date.now();
    batch.set(F.doc(db, "users", user.uid, "kv", docIdOf(k)), { v, t: meta[k], dev });
  });
  saveMeta();
  try { await batch.commit(); status("ok"); }
  catch (e) { keys.forEach((k) => dirty.add(k)); status("err"); console.warn("sync:", e); }
}

// ---------- 本棚の右上のログインの欄 ----------
const ID_DOMAIN = "@textbooks.example.com";
const ui = { login: null, logout: null };
let lastState = "", ready = false;   // ready: ログインの状態がわかってから欄を出す（それまで押しても何もできないので）
const esc = (t) => String(t).replace(/[<>&"]/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }[c]));
const ERR = {
  "auth/invalid-credential": "ID かパスワードがちがいます", "auth/wrong-password": "ID かパスワードがちがいます", "auth/user-not-found": "ID かパスワードがちがいます",
  "auth/invalid-login-credentials": "ID かパスワードがちがいます", "auth/email-already-in-use": "その ID はもう使われています。ログインしてください",
  "auth/weak-password": "パスワードは6文字以上にしてください", "auth/too-many-requests": "何度もまちがえたので、しばらく待ってからためしてください",
  "auth/network-request-failed": "インターネットにつながっていません", "auth/invalid-email": "ID に使えない文字があります",
  "auth/configuration-not-found": "ログインの設定（Firebase の Authentication）がまだです", "auth/operation-not-allowed": "ログインの設定（メール / パスワード）がまだです",
};
function status(s) { lastState = s; draw(); }
function draw() {
  const el = document.getElementById("acct");
  if (!el) return;
  if (!ready) { el.innerHTML = ""; return; }
  if (!user) {
    el.innerHTML = `<button type="button" class="acct-btn" aria-expanded="false" title="スマホと PC の記録を合わせる">☁ ログイン</button>`
      + `<form class="acct-menu acct-form" hidden autocomplete="on">`
      + `<p class="m">同じ ID とパスワードでログインすると、スマホと PC の記録（勉強時間・続き・練習問題・単語・付箋）がそろいます</p>`
      + `<label>ID<input name="loginid" autocomplete="username" autocapitalize="off" spellcheck="false" placeholder="半角の英数字（3文字以上）" required></label>`
      + `<label>パスワード<input name="loginpw" type="password" autocomplete="current-password" placeholder="6文字以上" required></label>`
      + `<p class="acct-err" hidden></p>`
      + `<div class="acct-row"><button type="submit" class="pri">ログイン</button><button type="button" class="acct-new">はじめて使う（登録）</button></div></form>`;
    const btn = el.querySelector(".acct-btn"), form = el.querySelector("form"), err = el.querySelector(".acct-err");
    btn.onclick = () => { form.hidden = !form.hidden; btn.setAttribute("aria-expanded", !form.hidden); if (!form.hidden) form.elements.loginid.focus(); };
    const go = async (isNew) => {
      const id = form.elements.loginid.value.trim().toLowerCase(), pw = form.elements.loginpw.value;
      err.hidden = true;
      if (!/^[a-z0-9][a-z0-9._-]{2,29}$/.test(id)) { err.textContent = "ID は半角の英数字（. _ - も可）で3〜30文字にしてください"; err.hidden = false; return; }
      if (pw.length < 6) { err.textContent = ERR["auth/weak-password"]; err.hidden = false; return; }
      form.querySelectorAll("button").forEach((b) => { b.disabled = true; });
      try { await ui.login(id, pw, isNew); }
      catch (e) { err.textContent = ERR[e.code] || "ログインできませんでした（" + e.code + "）"; err.hidden = false; }
      form.querySelectorAll("button").forEach((b) => { b.disabled = false; });
    };
    form.onsubmit = (e) => { e.preventDefault(); go(false); };
    el.querySelector(".acct-new").onclick = () => { form.elements.loginpw.setAttribute("autocomplete", "new-password"); go(true); };
    return;
  }
  const id = (user.email || "").replace(ID_DOMAIN, "");
  const label = lastState === "err" ? "⚠ 同期できません" : lastState === "sync" ? "同期中…" : "同期 ✓";
  el.innerHTML = `<button type="button" class="acct-btn on${lastState === "err" ? " err" : ""}" aria-expanded="false">☁ <span>${label}</span></button>`
    + `<div class="acct-menu" hidden><p><b>${esc(id)}</b> でログイン中</p><p class="m">スマホと PC の記録を合わせています</p><button type="button" class="acct-out">ログアウト</button></div>`;
  const btn = el.querySelector(".acct-btn"), menu = el.querySelector(".acct-menu");
  btn.onclick = () => { menu.hidden = !menu.hidden; btn.setAttribute("aria-expanded", !menu.hidden); };
  el.querySelector(".acct-out").onclick = () => ui.logout && ui.logout();
}
if (config) {
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", draw); else draw();
  document.addEventListener("click", (e) => { const el = document.getElementById("acct"); if (el && !el.contains(e.target)) { const m = el.querySelector(".acct-menu"); if (m) m.hidden = true; } });
}
