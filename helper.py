
def isOverLap(recPosActualTuple, recPosTargetTuple):
    #returns True if there are overlaps between the rectangles, False if not
    (act_x1, act_y1, act_x2, act_y2) = recPosActualTuple
    (tar_x1, tar_y1, tar_x2, tar_y2) = recPosTargetTuple
    if act_y2 > tar_y1 and act_x2 > tar_x1:
        return True
    return False