"""
Enable picking on the legend to toggle the legended line on and off
"""
import numpy as np
import matplotlib.pyplot as plt

import pylustrator
pylustrator.start()
#plt.ion()

#StartDragger()

t = np.arange(0.0, 0.2, 0.1)
y1 = 2*np.sin(2*np.pi*t)
y2 = 4*np.sin(2*np.pi*2*t)
fig = plt.figure(0, (18/2.54, 15/2.54))
"""
#fig, ax = plt.subplots()
plt.subplot(231)
line1, = plt.plot(t, y1, lw=2, color='red', label='1 HZ')

line2, = plt.plot(t, y2, lw=2, color='blue', label='2 HZ')
#leg = ax.legend(loc='upper left', fancybox=True, shadow=True)
#leg.get_frame().set_alpha(0.4)
"""
ax0 = plt.subplot(231, label="a")
#line1, = plt.plot(t, y1, lw=2, color='red', label='1 HZ')
#line2, = plt.plot(t, y2, lw=2, color='blue', label='2 HZ')

import matplotlib as mpl
p = mpl.patches.FancyArrowPatch((0.4, 0.2), (3.6, 3.3), arrowstyle="Simple,head_length=10,head_width=10,tail_width=2", shrinkA=0, shrinkB=0, facecolor="black", clip_on=False, zorder=2)
#p = mpl.patches.FancyArrowPatch((0.4, 0.2), (4.6, 4.3), arrowstyle="Simple,head_length=28,head_width=36,tail_width=20")
plt.gca().add_patch(p)
p.set_picker(True)
ax0.set_xlim(0, 5)
ax0.set_ylim(0, 5)

ax0 = plt.subplot(233, label="b")
line1, = plt.plot(t, y1, lw=2, color='red', label='1 HZ')
line2, = plt.plot(t, y2, lw=2, color='blue', label='2 HZ')
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.legend()

ax2 = plt.subplot(235, label="c")
a = np.arange(1000).reshape(20, 50)
plt.imshow(a)

ax1 = plt.axes([0.2, 0.2, 0.2, 0.2])#subplot(234)
line1, = plt.plot(t, y1, lw=2, color='red', label='1 HZ')
line2, = plt.plot(t, y2, lw=2, color='blue', label='2 HZ')
plt.axis("equal")
plt.legend()


from mpl_toolkits.axes_grid1.inset_locator import mark_inset
mark_inset(ax0, ax1, loc1=2, loc2=4, fc="none", lw=2, ec='r')

ax3 = plt.colorbar()

plt.axis()


plt.text(0, 0, "Heyhho", transform=ax2.transAxes, picker=True)
plt.text(10, 10, "Heyhho", transform=ax2.transData, picker=True)


#% start: automatic generated code from pylustrator
fig = plt.figure(0)
fig.ax_dict = {ax.get_label(): ax for ax in fig.axes}
fig.ax_dict["a"].get_yaxis().get_label().set_fontname("Palatino Linotype")
fig.ax_dict["a"].get_yaxis().get_label().set_style("italic")
fig.ax_dict["a"].get_yaxis().get_label().set_weight("normal")
fig.ax_dict["a"].get_yaxis().get_label().set_fontsize(28)
fig.ax_dict["a"].get_xaxis().get_label().set_fontsize(14)
fig.ax_dict["a"].set_position([0.086832, 0.563898, 0.227941, 0.350000])
fig.ax_dict["a"].set_xlabel("asdasd")
fig.ax_dict["a"].set_ylabel("asdasd")
fig.ax_dict["a"].spines['right'].set_visible(False)
fig.ax_dict["a"].spines['top'].set_visible(False)
fig.ax_dict["a"].add_patch(mpl.patches.FancyArrowPatch((0.0, 0.0), (2.5, 2.5), arrowstyle='Simple,head_length=10,head_width=10,tail_width=2', facecolor='black', clip_on=False, zorder=2))  # id=fig.ax_dict["a"].patches[2].new
fig.ax_dict["a"].patches[1].set_positions((0.7043331053719026, 2.1065375302663423), (0.7067055862705918, 4.606537530266349))
fig.ax_dict["a"].patches[1].set_edgecolor("#3377d1")
fig.ax_dict["a"].yaxis.labelpad = -1.920000
fig.ax_dict["a"].annotate('New Annotation', (-0.005000000000000001, -0.1902113032590307), (0.05, 1.902113032590307), arrowprops=dict(arrowstyle='->'))  # id=fig.ax_dict["a"].texts[0].new
fig.ax_dict["b"].set_position([0.426778, 0.563898, 0.255228, 0.350000])
fig.ax_dict["b"].spines['right'].set_visible(False)
fig.ax_dict["b"].spines['top'].set_visible(False)
fig.ax_dict["b"].set_xlabel("asd")
fig.ax_dict["b"].set_ylabel("axaxa")
fig.ax_dict["b"].yaxis.labelpad = -14.192532
fig.ax_dict["b"].xaxis.labelpad = -6.160000
fig.ax_dict["c"].set_position([0.398529, 0.377709, 0.227941, 0.109412])
fig.axes[3].set_position([0.174548, 0.287121, 0.160000, 0.109412])
fig.axes[3].set_xlabel("asas")
fig.axes[3].set_ylabel("yyy")
fig.axes[4].set_position([0.645424, 0.287121, 0.008333, 0.200000])
fig.ax_dict["a"].patches[0].set_positions((1.1747019678027741, 2.9383742857142856), (4.6843821043293286, 3.9295399515738207))
#% end: automatic generated code from pylustrator
#pylustrator.StartPylustrator()
plt.savefig("test.png")
plt.show()
#plt.show()