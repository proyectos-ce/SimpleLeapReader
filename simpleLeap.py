import Leap, sys, time, thread, math
import paho.mqtt.client as mqtt


class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    client = mqtt.Client("leapTavo")

    def on_init(self, controller):
        print("Initialized")
        self.client.connect("iot.eclipse.org", 1883, 60)

    def on_connect(self, controller):
        print("Motion Sensor Connected")

    def on_disconnect(self, controller):
        print("Motion Sensor Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        frame = controller.frame()
        # print (frame.id,"Is valid:",frame.is_valid)
        frameJson = {'frameId':frame.id, 'hands':[]}
        for hand in frame.hands:
            handtype = "left" if hand.is_left else "right"
            frameJson['hands'].append({'type':handtype, 'id':hand.id})
            print (handtype, hand.id, "{0:.2f}".format(hand.direction.x), "{0:.2f}".format(hand.direction.y), "{0:.2f}".format(hand.direction.z) )
            
        if(frame.hands):
            self.client.publish("leapLesco", str(frameJson))



def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    print("Press Enter to quit")

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == '__main__':
    main()
