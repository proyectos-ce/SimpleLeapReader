import Leap, sys
import paho.mqtt.client as mqtt
import json

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
        frameJson = {'valid':frame.is_valid,'frameId':frame.id, 'hands':[]}
        for hand in frame.hands:
            handtype = 0 if hand.is_left else 1
            handJson = {'valid':hand.is_valid,'type':handtype, 'id':hand.id, 'fingers':[]}
            handJson['direction']={'x':hand.direction.x, 'y':hand.direction.y,'z':hand.direction.z}
            for finger in hand.fingers:
                fingerJson={'valid':finger.is_valid,'bones':[],'type':finger.type, 'id':finger.id, 'direction':{'x':finger.direction.x,'y':finger.direction.y,'z':finger.direction.z}}
                for index in range(4):
                    fingerJson['bones'].append({'valid':finger.bone(index).is_valid,'type':finger.bone(index).type,'direction':{'x':finger.bone(index).direction.x,'y':finger.bone(index).direction.y,'z':finger.bone(index).direction.z} })
                handJson['fingers'].append(fingerJson)
            frameJson['hands'].append(handJson)
        if(frame.hands):
            self.client.publish("leapLesco", json.dumps(frameJson))
            print json.dumps(frameJson)


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
