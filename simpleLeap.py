import Leap, sys, time, thread, math

class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Motion Sensor Connected")

    def on_disconnect(self, controller):
        print("Motion Sensor Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        frame = controller.frame()
        print (frame.id,"Is valid:",frame.is_valid)
        for hand in frame.hands:
            handtype = "Left Hand" if hand.is_left else "Right Hand"
            print (handtype, hand.id, "{0:.2f}".format(hand.direction.x), "{0:.2f}".format(hand.direction.y), "{0:.2f}".format(hand.direction.z) )

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
