import cv2
import numpy as np
from skindetector import SkinDetector
import sys

if __name__ == "__main__":
    if (len(sys.argv)) < 2:
        file_path = "sample.jpg"
    else:
        file_path = sys.argv[1]

    # read image
    src = cv2.imread(file_path, 1)
    src = cv2.resize(src, (640, 480))
    cv2.imshow("Input", src)
    detector = SkinDetector(file_path, 1)
    thresh = detector.find_skin()
    thresh = cv2.resize(thresh, (640, 480))
    cv2.imshow("Binary", thresh)



    # find contours
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # create an empty black image
    drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
    color_contours = (0, 255, 0)  # color for contours
    color = (255, 0, 0)  # color for convex hull



    # draw contours
    cv2.drawContours(drawing, contours, -1,  color_contours, 2, 8, hierarchy)
    cv2.drawContours(src, contours, -1,  color_contours, 2, 8, hierarchy)

    cv2.imshow("contours", drawing)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # cv2.imshow("Before", drawing)
    # draw convex hull
    # cv2.drawContours(drawing, hull, ind, color, 2, 8)
    # cv2.drawContours(src, hull, ind, color, 2, 8)
    #
    # cv2.imshow("contour", drawing)
    # cnt = contours[ind]
    # hullBig = cv2.convexHull(cnt, returnPoints=False)
    #
    # valley = []
    # count = 0
    # defects = cv2.convexityDefects(cnt, hullBig)
    # for i in range(defects.shape[0]):
    #     s, e, f, d = defects[i, 0]  # Distance from edge
    #     start = tuple(c[s][0])
    #     end = tuple(c[e][0])
    #     far = tuple(c[f][0])  # Farthest point
    #     # if i == 0:
    #     #     cv2.circle(drawing, far, 5, [0, 0, 255], -1)
    #     #     cv2.circle(src, far, 5, [0, 0, 255], -1)
    #     # else:
    #     if d > 1000:
    #         count += 1
    #         # print(c[f])
    #         if count != 3 and count != 4:
    #             valley.append([c[f][0][0], c[f][0][1]])
    #             cv2.circle(drawing, far, 5, [0, 0, 255], -1)
    #             cv2.circle(src, far, 5, [0, 0, 255], -1)
    #
    # # print(defects)
    # # print(len(defects))
    # # print(thresh.shape)
    # # print(len(cnt))
    # # print(c)
    # # print(c.shape)
    # # print(thresh.shape)
    # # print(thresh)
    # # print(drawing.shape)
    # # print(drawing)
    # # print(cnt)
    # # print(hull[ind].shape)
    # # print(hull[ind])
    #
    # # for i in range(c.shape[0]):
    # #     for j in range(c.shape[1]):
    # #         if c[i][j][0] > 480:
    # #             print(c[i][j])
    # #             drawing[c[i][j][1], c[i][j][0]] = (0, 255, 255)
    #
    #
    # # Centroid
    # # M = cv2.moments(cnt)
    # # cX = int(M["m10"] / M["m00"])
    # # cY = int(M["m01"] / M["m00"])
    # # # draw center of the shape on the image
    # # cv2.circle(drawing, (cX, cY), 5, (0, 0, 255), -1)
    # # cv2.circle(src, (cX, cY), 5, (0, 0, 255), -1)
    # # valley.append([cX, cY])
    #
    #
    # # changing frame of reference to OpenGL
    # for i in range(len(valley)):
    #     valley[i][1] = 479 - valley[i][1]
    # print("Required coordinates wrt OPENgl:")
    # print(valley)
    #
    # cv2.imshow("Output", drawing)
    # # res = cv2.bitwise_and(drawing, src, mask=None)
    # # cv2.imshow("Output", src)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    #
    #
    # # pilot = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
    # # count = 0
    # # for i in range(c.shape[0]):
    # #     for j in range(c.shape[1]):
    # #         x = c[i][j][::-1]
    # #         print(x[0], x[1])
    # #         pilot[x[0], x[1]] = (0, 255, 255)
    # #         count += 1
    # #         if count > 200:
    # #             break
    # #     if count > 200:
    # #         break
    #
