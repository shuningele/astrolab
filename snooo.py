import snpy
import matplotlib.pyplot as plt
s = snpy.get_sn('sn2022vqz.txt')
model = "max_model"
sp="dm15"
s.choose_model(model, stype=sp)
s.set_restbands()
s.fit()
s.fitMCMC()
s.plot(single=1, offset=True)
plt.show()
print(s.summary())
s.save("sn2022vqz.snpy")
s.dump_lc()

