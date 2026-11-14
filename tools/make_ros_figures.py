#!/usr/bin/env python3
"""ROS 2 と ArduPilot の教科書（books/ros）の図を SVG で作る。

    python3 tools/make_ros_figures.py

箱と矢印の描き方・色は make_study_figures.py と同じものを使う。
"""
from pathlib import Path

from make_cow_figures import MUTED, S1, S2, S3, S4, TEXT, TEXT2, svg, t
from make_study_figures import AH, arrow, box

OUT = Path(__file__).resolve().parent.parent / "books" / "ros" / "images"


def fig_graph():
    """ノード・トピック・サービスの関係"""
    b = [t(410, 28, "ROS 2 のノードとトピック / Nodes and topics", 14, "middle", TEXT, 700)]
    b += box(30, 70, 170, 60, "talker", S1, "ノード（送る側）")
    b += box(320, 76, 180, 48, "/chatter", S3, "トピック（String）", size=13)
    b += box(620, 40, 170, 56, "listener", S1, "ノード（受け取る側）")
    b += box(620, 112, 170, 56, "logger", S1, "ノード（同じものを受け取る）")
    b += arrow(204, 100, 314, 100, "publish", 259, 90)
    b += arrow(504, 92, 614, 70, "subscribe", 560, 66)
    b += arrow(504, 108, 614, 136, None)
    b.append(t(410, 160, "1つのトピックに、送る側も受け取る側も何個でもつなげる", 12, "middle", TEXT2))
    b += box(30, 200, 170, 60, "client", S2, "ノード（頼む側）")
    b += box(620, 200, 170, 60, "server", S2, "ノード（答える側）")
    b += arrow(204, 220, 614, 220, "request（/add_two_ints）", 409, 211)
    b.append(f'<line x1="614" y1="242" x2="206" y2="242" stroke="{TEXT2}" stroke-width="1.6" marker-end="url(#ah)"/>')
    b.append(t(409, 258, "response", 12, "middle", TEXT, 700, ' font-family="ui-monospace, monospace"'))
    b.append(t(410, 290, "サービスは「1回頼んで、1回答えをもらう」。トピックは「流しっぱなし」", 12.5, "middle", TEXT, 700))
    return svg(820, 310, [AH] + b)


def fig_system():
    """フライトコントローラー・コンパニオンコンピューター・地上局のつながり"""
    b = [t(410, 28, "ArduPilot と ROS 2 のつながり / ArduPilot + ROS 2", 14, "middle", TEXT, 700)]
    # 機体の中
    b.append(f'<rect x="20" y="50" width="560" height="250" rx="12" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="6 4"/>')
    b.append(t(34, 70, "機体（ドローン・ローバー）", 12, "start", TEXT2, 700))
    b += box(40, 90, 200, 86, "フライトコントローラー", S2, "ArduPilot（AP_DDS 入り）")
    b.append(t(92, 200, "Pixhawk など（H7 の CPU）", 11.5, "start", TEXT2))
    b += box(360, 84, 200, 56, "micro-ROS Agent", S3, "DDS の中継")
    b += box(360, 160, 200, 56, "自分の ROS 2 ノード", S1, "Python・C++")
    b += box(360, 230, 200, 50, "RViz・ナビ・カメラ", S1, None, size=12.5)
    b.append(t(460, 76, "コンパニオンコンピューター（Jetson・ラズパイ）", 11, "middle", TEXT2))
    b += arrow(244, 112, 354, 112, "XRCE-DDS", 299, 103)
    b.append(t(299, 130, "シリアル / UDP", 11, "middle", TEXT2))
    b += arrow(460, 144, 460, 156, None)
    b.append(t(468, 152, "ROS 2（DDS）", 11, "start", TEXT2))
    # センサー
    b += box(40, 216, 200, 64, "GPS・IMU・コンパス", S4, "モーター・ESC・RC 受信機", opacity=0.14, size=12.5)
    b.append(f'<line x1="70" y1="180" x2="70" y2="212" stroke="{TEXT2}" stroke-width="1.6" marker-start="url(#ah)" marker-end="url(#ah)"/>')
    # 地上局
    b += box(620, 100, 180, 70, "地上局（GCS）", S2, "QGroundControl など", opacity=0.10)
    b.append(f'<path d="M244 160 H 300 V 292 H 700 V 174" fill="none" stroke="{TEXT2}" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#ah)"/>')
    b.append(t(690, 236, "MAVLink", 12, "end", TEXT, 700, ' font-family="ui-monospace, monospace"'))
    b.append(t(690, 254, "（テレメトリ無線）", 11.5, "end", TEXT2))
    b.append(t(410, 336, "飛ぶための計算はフライトコントローラー、考える仕事はコンパニオンコンピューター", 12.5, "middle", TEXT, 700))
    return svg(820, 360, [AH] + b)


FIGS = {"ros-graph.svg": fig_graph, "ardupilot-ros2.svg": fig_system}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGS.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    print(f"{len(FIGS)} 枚の図を書き出しました")
