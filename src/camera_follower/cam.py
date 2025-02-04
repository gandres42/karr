import cv2

cap_shape = (480, 640, 3)
cap = cv2.VideoCapture('/dev/video0')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_shape[1])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_shape[0])

# Get the default frame width and height
while True:
    ret, frame = cap.read()
    frame = frame.reshape(cap_shape)
    # Display the captured frame
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cap.release()
cv2.destroyAllWindows()