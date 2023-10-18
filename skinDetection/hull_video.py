import cv2
import numpy as np
import argparse
from skindetector import SkinDetector

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the (optional) video file")
    args = vars(ap.parse_args())
    # define the upper and lower boundaries of the HSV pixel
    # intensities to be considered 'skin'
    # lower = np.array([0, 48, 80], dtype="uint8")
    # upper = np.array([20, 255, 255], dtype="uint8")

    # if a video path was not supplied, grab the reference
    # to the gray
    if not args.get("video", False):
        camera = cv2.VideoCapture(0)
    # otherwise, load the video
    else:
        camera = cv2.VideoCapture(args["video"])
    # keep looping over the frames in the video
    while True:
        (grabbed, frame) = camera.read()
        # if we are viewing a video and we did not grab a
        # frame, then we have reached the end of the video
        if args.get("video") and not grabbed:
            break
        # frame = imutils.resize(frame, width=400)
        frame = cv2.resize(frame, (640, 480))
        detector = SkinDetector(frame, 2)
        thresh = detector.find_skin()
        thresh = cv2.resize(thresh, (640, 480))
        cv2.imshow("Binary", thresh)
        # find contours
        _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        c = max(contours, key=cv2.contourArea)
        for i in range(len(contours)):
            if len(contours[i]) == len(c):
                ind = i
                break

        # create hull array for convexHull points
        hull = []
        # calculate points for each contour
        for i in range(len(contours)):
            hull.append(cv2.convexHull(contours[i], False))


        # create an empty black image
        drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)

        color_contours = (0, 255, 0)  # color for contours
        color = (255, 0, 0)  # color for convex hull
        # draw contours
        cv2.drawContours(drawing, contours, ind, color_contours, 2, 8, hierarchy)
        cv2.drawContours(frame, contours, ind, color_contours, 2, 8, hierarchy)
        # draw convex hull
        cv2.drawContours(drawing, hull, ind, color, 2, 8)
        cv2.drawContours(frame, hull, ind, color, 2, 8)

        cnt = contours[ind]
        # print(cnt.shape)
        hullBig = cv2.convexHull(cnt, returnPoints=False)
        # print(hullBig.shape)

        defects = cv2.convexityDefects(cnt, hullBig)

        # for i in range(defects.shape[0]):
        #     s, e, f, d = defects[i, 0]
        #     start = tuple(c[s][0])
        #     end = tuple(c[e][0])
        #     far = tuple(c[f][0])
        #     # cv2.line(drawing, start, end, [0, 255, 0], 2)
        #     # cv2.line(frame, start, end, [0, 255, 0], 2)
        #     cv2.circle(drawing, far, 5, [0, 0, 255], -1)
        #     cv2.circle(frame, far, 5, [0, 0, 255], -1)

        # For only valley points
        valley = []
        count = 0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]  # Distance from edge
            start = tuple(c[s][0])
            end = tuple(c[e][0])
            far = tuple(c[f][0])  # Farthest point
            # if i == 0:
            #     cv2.circle(drawing, far, 5, [0, 0, 255], -1)
            #     cv2.circle(frame, far, 5, [0, 0, 255], -1)
            # else:
            if d > 15000:
                # print(c[f])
                valley.append([c[f][0][0], c[f][0][1]])
                cv2.circle(drawing, far, 5, [0, 0, 255], -1)
                cv2.circle(frame, far, 5, [0, 0, 255], -1)


        # # Centroid
        # M = cv2.moments(cnt)
        # cX = int(M["m10"] / M["m00"])
        # cY = int(M["m01"] / M["m00"])
        # # draw center of the shape on the image
        # cv2.circle(drawing, (cX, cY), 5, (0, 0, 255), -1)
        # cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
        # cY = int(M["m01"] / M["m00"])

        # changing frame of reference to OpenGL
        for i in range(len(valley)):
            valley[i][1] = 479 - valley[i][1]
        print("Required coordinates wrt OPENgl:")
        print(valley)

        cv2.imshow("Mask", drawing)
        cv2.imshow("Output", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()