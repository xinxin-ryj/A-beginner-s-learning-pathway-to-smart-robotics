from pyb import UART, Pin,Timer
import sensor,time, pyb
import colorBlock,aprilTag,apriltagNumSort,faceTrack

color_block = colorBlock.ColorBlock()
april_tag = aprilTag.AprilTag()
april_tag_num_sort = apriltagNumSort.AprilTagNumSort()
face_track = faceTrack.FaceTrack()

led = pyb.LED(3)

uart = UART(3,115200)   #设置串口波特率，与stm32一致
uart.init(115200, bits=8, parity=None, stop=1 )
uart.write("$KMS:0,100,70,1000!\n")

tim = Timer(4, freq=1000) # Frequency in Hz
led_dac = tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=50)
led_dac.pulse_width_percent(0)

run_app_status=0

uart.write("#openmv reset\n\n!")

#调整中点，用于调整机械臂抓取物块中点
#如果机械臂抓取偏左，mid_block_cx减小，反之增加
#如果机械臂抓取偏前，mid_block_cy减小，反之增加
#如果机械臂抓取偏下或偏上，就调节2号舵机偏差
mid_block_cx=80.5
mid_block_cy=60.5

def beep():
    uart.write("$BEEP!\n")#发送蜂鸣器鸣叫指令
    led.on()            #亮灯
    time.sleep_ms(100)  #延时150ms
    led.off()           #暗灯
    time.sleep_ms(100)


while(True):
    if uart.any():#接收指令
        try:#用来判断串口数据异常
            string = uart.read()
            print(string,isinstance(string.decode(), str))
            if string:
                string = string.decode()
                #print(string,isinstance(string, str),string.find("#start_led!"))
                if string.find("#StartLed!") >= 0 :#开灯指令
                    led_dac.pulse_width_percent(100)
                    beep()
                elif string.find("#StopLed!") >= 0 :#关灯指令
                    led_dac.pulse_width_percent(0)
                    beep()
                elif string.find("#RunStop!") >= 0 :#停止所有运行并复位
                    run_app_status=0
                    led_dac.pulse_width_percent(0)
                    beep()
                elif string.find("#ColorSort!") >= 0 :#色块分拣
                    run_app_status=1
                    color_block.init(mid_block_cx,mid_block_cy)
                    beep()
                elif string.find("#ColorStack!") >= 0 :#色块码垛
                    run_app_status=2
                    color_block.init(mid_block_cx,mid_block_cy)
                    beep()
                elif string.find("#FaceTrack!") >= 0 :#人脸识别
                    run_app_status=3
                    face_track.init()
                    beep()
                elif string.find("#ColorTrack!") >= 0 :#颜色追踪
                    run_app_status=4
                    color_block.init()
                    beep()
                elif string.find("#ApriltagSort!") >= 0 :#二维码标签分拣
                    run_app_status=5
                    april_tag.init(mid_block_cx,mid_block_cy)
                    beep()
                elif string.find("#ApriltagStack!") >= 0 :#二维码标签码垛
                    run_app_status=6
                    april_tag.init(mid_block_cx,mid_block_cy)
                    beep()
                elif string.find("#ApriltagNumSort!") >= 0 :#二维码标签数字分拣
                    run_app_status=7
                    april_tag_num_sort.init(mid_block_cx,mid_block_cy)
                    beep()
        except Exception as e:#串口数据异常进入
            print('Error:', e)

    if run_app_status==1:
        color_block.run_sort()#运行分拣色块功能
    elif run_app_status==2:
        color_block.run_stack()#运行物块码垛功能
    elif run_app_status==3:
        face_track.run_track()#运行人脸追踪
    elif run_app_status==4:
        color_block.run_track()#运行颜色追踪
    elif run_app_status==5:
        april_tag.run_sort()#运行标签分拣
    elif run_app_status==6:
        april_tag.run_stack()#运行标签码垛
    elif run_app_status==7:
        april_tag_num_sort.run_sort()#数字分拣




