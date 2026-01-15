from pyb import UART, Pin,Timer
import time, pyb
import aprilTag

led = pyb.LED(3)

april_tag = aprilTag.AprilTag()

uart = UART(3,115200)   #设置串口波特率，与stm32一致
uart.init(115200, bits=8, parity=None, stop=1 )

tim = Timer(4, freq=1000) # Frequency in Hz
led_dac = tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=50)
led_dac.pulse_width_percent(100)

print("\n\nopenmv reset\n\n")

#调整中点，用于调整机械臂抓取物块中点
#如果机械臂抓取偏右，mid_block_cx减小，反之增加
#如果机械臂抓取偏前，mid_block_cy减小，反之增加
#如果机械臂抓取偏下或偏上，就调节机械臂第2，3个舵机偏差
mid_block_cx=80.5
mid_block_cy=60.5


def beep():
    uart.write("$BEEP!\n")#发送蜂鸣器鸣叫指令
    led.on()            #亮灯
    time.sleep_ms(100)     #延时150ms
    led.off()           #暗灯
    time.sleep_ms(100)

april_tag.init(mid_block_cx,mid_block_cy)
beep()
while(1):
    april_tag.run_stack()
    if uart.any():#接收指令
        try:#用来判断串口数据异常
            string = uart.read()
            if string:
                string = string.decode()
                print(string)
        except Exception as e:#串口数据异常进入
            print('Error:', e)




