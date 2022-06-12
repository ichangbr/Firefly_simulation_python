from Lucpy import Hive
import numpy as np
import matplotlib.pyplot as plt

r = np.arange(0,1.4,0.05)

amp_mean_list = []
for radius in r:
    amp_list = []
    for _ in range(50):
        prov = Hive(radius = radius)
        res,_ = prov.analytical_loop(mode = 'last_50')
        amplitude = (max(res)-min(res))/2
        amp_list.append(amplitude)
    amp_mean_list.append(np.mean(amp_list))
    print(radius)

plt.scatter(r,amp_mean_list)
plt.show()

print(r[amp_mean_list.index(max(amp_mean_list))])
