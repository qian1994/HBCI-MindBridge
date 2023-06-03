import random
from psychopy import visual, core
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
from brainflow.board_shim import BoardShim, BrainFlowInputParams
import time
import datetime
# 创建刺激窗口
boardId = 532
win = visual.Window(size=(800, 600), fullscr=True)
params = BrainFlowInputParams()
params.ip_port = 9521 + random.randint(1, 100)
params.ip_address = '192.168.31.197'
board = BoardShim(int(boardId), params)

board.prepare_session()
time.sleep(1)
board.start_stream()

# 定义刺激图片文件名列表
image_files = ['./assets/2size/b/1 ({}).jpg'.format(i+1) for i in range(96)]

# 创建刺激对象列表
stimuli = []
for file in image_files:
    stimulus = visual.ImageStim(win, image=file)
    stimuli.append(stimulus)


image_files_o = ['./assets/2size/o/1 ({}).jpg'.format(i+1) for i in range(24)]

stimuli_o = []
for file in image_files_o:
    stimulus = visual.ImageStim(win, image=file)
    stimuli_o.append(stimulus)
# 定义刺激闪烁频率（Hz）
stim_frequency = 12

# 定义刺激呈现时间（秒）
stim_duration = 25

# 定义每五次闪烁中其他图片的位置
other_image_position = [4, 9, 14, 19]

# 计算每个刺激帧的持续时间
frame_dur = 1.0 / stim_frequency

# 刺激呈现循环
frame_count = 0
while frame_count * frame_dur < stim_duration:
    if frame_count % 2 == 0:
        win.flip()
        core.wait(frame_dur)
        frame_count += 1
        continue
    if frame_count % 6 == 1:
        # 随机选择一个其他图片
        other_image = random.choice(stimuli[:])
        other_image.draw()
    else:
        # 随机选择一个A刺激图片
        A_image = random.choice(stimuli_o[:])
        A_image.draw()
    win.flip()
    core.wait(frame_dur)
    frame_count += 1
# 关闭刺激窗口
win.close()

board.stop_stream()
data = board.get_board_data()
time_now = datetime.datetime.now()
time_string = time_now.strftime("%Y_%m_%d_%H_%M_%S")
MindBridgefileName = time_string + '.csv'
DataFilter.write_file(
            data=data, file_name=MindBridgefileName, file_mode='w')
board.release_all_sessions()

