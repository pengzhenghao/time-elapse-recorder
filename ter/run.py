"""
by PENG Zhenghao
"""

import argparse

from ter.time_elapse_recorder import TimeElapseRecorder

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--interval', type=float, default=1.0,
        help="Interval between two frames, in seconds. Default: 1"
    )
    parser.add_argument(
        '--output-fps', type=int, default=30,
        help="The frames per second in the output video file. Default: 30"
    )
    parser.add_argument(
        '--display-fps', type=int, default=5,
        help="The frames per second in display window. Default: 5"
    )
    args = parser.parse_args()
    ter = TimeElapseRecorder(interval=args.interval, output_fps=args.output_fps, display_fps=args.display_fps)
    ter.run()
    ter.close()
