from xml.dom import minidom
import os
import xmltodict
from typing import List

class Position:
    def __init__(self, x : float, y : float, z : float):
        self.x = x
        self.y = y
        self.z = z 

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"


class PositionToDepth:
    def __init__(self, x : float, y : float, depth : float, player_index : int):
        self.x = x
        self.y = y
        self.depth = depth
        self.player_index = player_index

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.depth) + ", " + str(self.player_index) + ")"


class PositionToColor:
    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Joint:
    def __init__(self, position : Position, joint_type : str,  position_to_depth : PositionToDepth, position_to_color : PositionToColor):
        self.position = position
        self.joint_type = joint_type
        self.position_to_depth = position_to_depth
        self.position_to_color = position_to_color

    def __str__(self):
        return "(" + str(self.position) + ", " + str(self.joint_type) + str(self.position_to_depth) + str(self.position_to_color) + ")"    

    def __repr__(self):
        return "(" + str(self.position) + ", " + str(self.joint_type) + str(self.position_to_depth) + str(self.position_to_color) + ")"


class Skeleton:
    def __init__(self, skeleton : str, position : Position, joints : List[Joint]):
        self.skeleton = skeleton
        self.position = position
        self.joints = joints

    def __str__(self):
        return "( " + self.skeleton + ", " + str(self.position) + ", " + str(self.joints) + ")"    

    def __repr__(self):
        return "( " + self.skeleton + ", " + str(self.position) + ", " + str(self.joints) + ")"     


class KinectOutput:
    def __init__(self, kinect_output_str, skeletons : List[Skeleton]):
        self.kinect_output_str = kinect_output_str
        self.skeletons = skeletons

    def __str__(self):
        return "( " + str(self.kinect_output_str) + ", " + str(self.skeletons) + ")"

    def __repr__(self):
        return "( " + str(self.kinect_output_str) + ", " + str(self.skeletons) + "\n" + ")"


def get_array_object_from_dir_path(dir_path: str):
    skeleton_list = []
    kinect_output_list = []
    joint_list = []

    for kinect_output in os.listdir(dir_path):
        skeleton_path = os.path.join(dir_path, kinect_output, "Skeleton")
        

        for skeleton_index in os.listdir(skeleton_path):
            with open(os.path.join(skeleton_path, skeleton_index)) as f:
                skeleton_xml = f.read()
                skeleton_xml_parsed = xmltodict.parse(skeleton_xml)

                x = float(skeleton_xml_parsed['ArrayOfSkeleton']['Skeleton'][0]["Position"]["X"])
                y = float(skeleton_xml_parsed['ArrayOfSkeleton']['Skeleton'][0]["Position"]["Y"])
                z = float(skeleton_xml_parsed['ArrayOfSkeleton']['Skeleton'][0]["Position"]["Z"])

                position = Position(x, y, z)

                joints_holder_index = None

                for index in range(len(skeleton_xml_parsed['ArrayOfSkeleton']['Skeleton'])):
                    if 'Joints' in skeleton_xml_parsed['ArrayOfSkeleton']['Skeleton'][index]:
                        joints_holder_index = index
                        break
                
                if joints_holder_index is None:
                    continue

                for skeleton_data in skeleton_xml_parsed['ArrayOfSkeleton']['Skeleton'][joints_holder_index]['Joints']['Joint']:
                    position = Position(float(skeleton_data["Position"]["X"]), float(skeleton_data["Position"]["Y"]), float(skeleton_data["Position"]["Z"]))
                    joint_type = skeleton_data["JointType"]
                    position_to_depth = PositionToDepth(float(skeleton_data["PositionToDepth"]["X"]), float(skeleton_data["PositionToDepth"]["Y"]), float(skeleton_data["PositionToDepth"]["Depth"]), float(skeleton_data["PositionToDepth"]["PlayerIndex"]))
                    position_to_color = PositionToColor(float(skeleton_data["PositionToColor"]["X"]), float(skeleton_data["PositionToColor"]["Y"]))
                    
                    joint_list.append(Joint(position, joint_type, position_to_depth, position_to_color))
                
            skeleton_list.append(Skeleton(skeleton_index, position, joint_list))  
            joint_list = []  
        
        kinect_output_list.append(KinectOutput(kinect_output, skeleton_list))
    return kinect_output_list


if __name__ == "__main__":
    pass