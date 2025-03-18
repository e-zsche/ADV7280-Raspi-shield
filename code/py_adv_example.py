from lib import adv7280_ctrl

adv = adv7280_ctrl.ADV7280()

adv.set_CTI(True)
adv.set_CTI_threshold(127)

adv.set_noise_reduction(False)
adv.set_noise_reduction_threshold(0)

adv.set_C_shaping_filter("Wideband mode")

adv.set_alpha_blend("sharpest")
