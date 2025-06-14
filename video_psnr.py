# Install OpenCV if needed: pip install opencv-python
import cv2
import torch
import numpy as np
import sys

def psnr_torch(img1, img2):
    mse = torch.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 1.0
    return 20 * torch.log10(torch.tensor(PIXEL_MAX)) - 10 * torch.log10(mse)

def video_psnr(video_path1, video_path2):
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    psnr_list = []

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        if not ret1 or not ret2:
            break
        frame1 = torch.from_numpy(frame1.astype(np.float32) / 255.0).permute(2, 0, 1)
        frame2 = torch.from_numpy(frame2.astype(np.float32) / 255.0).permute(2, 0, 1)
        psnr_val = psnr_torch(frame1, frame2)
        psnr_list.append(psnr_val.item())

    cap1.release()
    cap2.release()
    return psnr_list, np.mean(psnr_list)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python video_psnr.py file1 file2")
        sys.exit(1)
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    psnr_per_frame, avg_psnr = video_psnr(file1, file2)
    print(f"Average PSNR: {avg_psnr}")