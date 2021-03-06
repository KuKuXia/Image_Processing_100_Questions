import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read image
img = cv2.imread("./imori.jpg").astype(np.float32)
H, W, C = img.shape

# Gray scale
gray = 0.2126 * img[..., 2] + 0.7152 * img[..., 1] + 0.0722 * img[..., 0]

# DCT
T = 8
K = 8
X = np.zeros((H, W), dtype=np.float32)

#ind_x = np.tile(np.arange(T), (T, 1))
#ind_y = np.arange(T).repeat(T).reshape(T, -1)
#dct = np.ones_like(ind_x, dtype=np.float32)
#dct[:, 0] /= np.sqrt(2)
#dct[0] /= np.sqrt(2)


def w(x, y, u, v):
    cu = 1.
    cv = 1.
    if u == 0:
        cu /= np.sqrt(2)
    if v == 0:
        cv /= np.sqrt(2)
    theta = np.pi / (2 * T)
    return ((2 * cu * cv / T) * np.cos((2*x+1)*u*theta) * np.cos((2*y+1)*v*theta))


for yi in range(0, H, T):
    for xi in range(0, W, T):
        for v in range(T):
            for u in range(T):
                for y in range(T):
                    for x in range(T):
                        X[v+yi, u+xi] += gray[y+yi, x+xi] * w(x, y, u, v)
                """
                _x = ind_x + xi * T
                _y = ind_y + yi * T
                _u = u + xi * T
                _v = v + yi * T
                X[_v, _u] = np.sum(C * gray[_y, _x] * np.cos((2*ind_x+1)*u*np.pi/(2*T)) * np.cos((2*indy+1)*v*np.pi/(2*T)))
                """

# IDCT
out = np.zeros((H, W), dtype=np.float32)

for yi in range(0, H, T):
    for xi in range(0, W, T):
        for y in range(T):
            for x in range(T):
                for v in range(K):
                    for u in range(K):
                        out[y+yi, x+xi] += X[v+yi, u+xi] * w(x, y, u, v)
                """
                _u = ind_x + xi * T
                _v = ind_y + yi * T
                _x = x + yi * T
                _y = y + xi * T
                out[_y, _x] = np.sum(C * X[_v, _u] * np.cos((2*x+1)*ind_x*np.pi/(2*T)) * np.cos((2*y+1)*indy*np.pi/(2*T))) * 4. / (T ** 2)
                """
out[out > 255] = 255
out = np.round(out).astype(np.uint8)

# Save result
cv2.imshow("result", out)
cv2.imwrite("out.jpg", out)

# Wait until a key pressed
cv2.waitKey(0)

# Destroy all the windows opened before
cv2.destroyAllWindows()
