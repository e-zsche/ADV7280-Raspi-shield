from subprocess import check_output
from adv7280_register_definitions import *
from adv7280_reg_val_dicts import *

"""
super hacky python class to control ADV7280-M device while running
uses i2cget and i2cset command line utilities to get / set registers

class functions:
set_CTI
set_CTI_threshold
set_alpha_blend
set_noise_reduction
set_noise_reduction_threshold

set_color_kill
set_color_kill_threshold
set_peaking_gain

set_C_shaping_filter
set_Y_shaping_filter

set_chroma_autogain
set_chroma_gain
set_luma_autogain
set_luma_gain

set_comb_filter_PAL
set_luma_comb_mode
set_chroma_comb_mode
set_chroma_comb_taps

set_brightness
set_contrast
set_hue

set_input
"""

class ADV7280():
    def __init__(self):
        self.addr = 0x21
        self.i2cbus = "10"

    def set_hue(self, hue):
        if hue < 0 or hue > 255:
            return
        val = self.__read_reg(ADV_REG_HUE)
        new_val = self.__set_bits_in_val(val, hue, 0xff)
        self.__write_reg(ADV_REG_HUE, new_val)

    def set_brightness(self, brightness):
        if brightness < 0 or brightness > 255:
            return
        val = self.__read_reg(ADV_REG_BRIGHTNESS)
        new_val = self.__set_bits_in_val(val, brightness, 0xff)
        self.__write_reg(ADV_REG_BRIGHTNESS, new_val)

    def set_contrast(self, contrast):
        if contrast < 0 or contrast > 255:
            return
        val = self.__read_reg(ADV_REG_CONTRAST)
        new_val = self.__set_bits_in_val(val, contrast, 0xff)
        self.__write_reg(ADV_REG_CONTRAST, new_val)

    def set_saturation_Cb(self, sat):
        if sat < 0 or sat > 255:
            return
        val = self.__read_reg(ADV_REG_SD_SATURATION_CB_CHANNEL)
        new_val = self.__set_bits_in_val(val, sat, 0xff)
        self.__write_reg(ADV_REG_SD_SATURATION_CB_CHANNEL, new_val)

    def set_saturation_Cr(self, sat):
        if sat < 0 or sat > 255:
            return
        val = self.__read_reg(ADV_REG_SD_SATURATION_CR_CHANNEL)
        new_val = self.__set_bits_in_val(val, sat, 0xff)
        self.__write_reg(ADV_REG_SD_SATURATION_CR_CHANNEL, new_val)

    def set_input(self, input_num: int):
        if input_num > 4 or input_num < 1:
            return
        val = self.__read_reg(ADV_REG_INPUT_CONTROL)
        val = self.__set_bits_in_val(val, 1<<input_num, 0xf)
        self.__write_reg(ADV_REG_INPUT_CONTROL, val)

    def set_Y_shaping_filter(self, filter):
        """
        sets a filter shape for luma processing.
        possible filters are stored in the
        self.ADV_Y_SHAPING_FILTER_MODES dict
        """
        if filter in ADV_Y_SHAPING_FILTER_MODES.values():
            filter_bits = filter
        elif filter in ADV_Y_SHAPING_FILTER_MODES.keys():
            filter_bits = ADV_Y_SHAPING_FILTER_MODES[filter]
        else:
            return
        val = self.__read_reg(ADV_REG_SHAPING_FILTER_CONTROL_1)
        new_val = self.__set_bits_in_val(val, filter_bits, 0x1f)
        self.__write_reg(ADV_REG_SHAPING_FILTER_CONTROL_1, new_val)

    def set_C_shaping_filter(self, filter):
        """
        sets a filter shape for chroma processing.
        possible filters are stored in the
        self.ADV_Y_SHAPING_FILTER_MODES dict
        """
        if filter in ADV_C_SHAPING_FILTER_MODES.values():
            filter_bits = filter
        elif filter in ADV_C_SHAPING_FILTER_MODES.keys():
            filter_bits = ADV_C_SHAPING_FILTER_MODES[filter]
        else:
            return
        val = self.__read_reg(ADV_REG_SHAPING_FILTER_CONTROL_1)
        new_val = self.__set_bits_in_val(val, filter_bits<<5, 0x7<<5)
        self.__write_reg(ADV_REG_SHAPING_FILTER_CONTROL_1, new_val)

    def set_comb_filter_PAL(self, filter):
        if filter in ADV_COMB_FILTER_PAL_MODE.values():
            filter_bits = filter
        elif filter in ADV_COMB_FILTER_PAL_MODE.keys():
            filter_bits = ADV_COMB_FILTER_PAL_MODE[filter]
        else:
            return
        val = self.__read_reg(ADV_REG_COMB_FILTER_CONTROL)
        new_val = self.__set_bits_in_val(val, filter_bits, 0x3)
        self.__write_reg(ADV_REG_SHAPING_FILTER_CONTROL_1, new_val)

    def set_color_kill(self, is_kill: bool):
        if is_kill > 1 or is_kill < 0:
            return
        val = self.__read_reg(ADV_REG_MISC_GAIN_CONTROL)
        new_val = self.__set_bits_in_val(val, bool(is_kill)<<6, 1<<6)
        self.__write_reg(ADV_REG_MISC_GAIN_CONTROL, new_val)

    def set_color_kill_threshold(self, threshold):
        """
        only possible if color kill is enabled
        """
        if threshold in ADV_COLOR_KILL_THRESHOLD.values():
            thresh_bits = threshold
        elif threshold in ADV_COLOR_KILL_THRESHOLD.keys():
            thresh_bits = ADV_COLOR_KILL_THRESHOLD[threshold]
        else:
            return
        val = self.__read_reg(ADV_REG_MANUAL_WINDOW_CONTROL)
        new_val = self.__set_bits_in_val(val, thresh_bits<<4, 0x7<<4)
        self.__write_reg(ADV_REG_MANUAL_WINDOW_CONTROL, new_val)

    def set_chroma_autogain(self, gain_setting: bool):
        if gain_setting in ADV_CHROMA_AGC_MODE.values():
            gain_bits = filter
        elif gain_setting in ADV_CHROMA_AGC_MODE.keys():
            gain_bits = ADV_CHROMA_AGC_MODE[gain_setting]
        else:
            return
        val = self.__read_reg(ADV_REG_AGC_MODE_CONTROL)
        new_val = self.__set_bits_in_val(val, gain_bits, 0x3)
        self.__write_reg(ADV_REG_AGC_MODE_CONTROL, new_val)

    def set_luma_autogain(self, gain_setting: bool):
        if gain_setting in ADV_LUMA_AGC_MODE.values():
            gain_bits = filter
        elif gain_setting in ADV_LUMA_AGC_MODE.keys():
            gain_bits = ADV_LUMA_AGC_MODE[gain_setting]
        else:
            return
        val = self.__read_reg(ADV_REG_AGC_MODE_CONTROL)
        new_val = self.__set_bits_in_val(val, gain_bits<<4, 0x7<<4)
        self.__write_reg(ADV_REG_AGC_MODE_CONTROL, new_val)

    def set_chroma_gain(self, gain):
        """
        only possible if chroma gain is set to manual
        """
        if gain < 0 or gain > 4095:
            return
        val = self.__read_reg(ADV_REG_CHROMA_GAIN_CONTROL_1)
        upper_val = self.__set_bits_in_val(val, gain>>8, 0xf)
        # write upper bits
        self.__write_reg(ADV_REG_CHROMA_GAIN_CONTROL_1, upper_val)
        # write lower bits
        self.__write_reg(ADV_REG_CHROMA_GAIN_CONTROL_2, gain&0xff)

    def set_luma_gain(self, gain):
        """
        only possible if luma gain is set to manual
        """
        if gain < 1024 or gain > 4095:
            return
        # write upper bits
        val = self.__read_reg(ADV_REG_LUMA_GAIN_CONTROL_1)
        upper_val = self.__set_bits_in_val(val, gain>>8, 0xf)
        self.__write_reg(ADV_REG_LUMA_GAIN_CONTROL_1, upper_val)
        # write lower bits
        self.__write_reg(ADV_REG_LUMA_GAIN_CONTROL_2, gain&0xff)

    def set_luma_comb_mode(self, mode):
        if mode in ADV_LUMA_COMB_MODE.values():
            mode_bits = mode
        elif mode in ADV_LUMA_COMB_MODE.keys():
            mode_bits = ADV_LUMA_COMB_MODE[mode]
        else:
            return
        val = self.__read_reg(ADV_REG_PAL_COMB_CONTROL)
        new_val = self.__set_bits_in_val(val, mode_bits, 0x7)
        self.__write_reg(ADV_REG_PAL_COMB_CONTROL, new_val)

    def set_chroma_comb_mode(self, mode):
        if mode in ADV_CHROMA_COMB_MODE.values():
            mode_bits = filter
        elif mode in ADV_CHROMA_COMB_MODE.keys():
            mode_bits = ADV_CHROMA_COMB_MODE[mode]
        else:
            return
        val = self.__read_reg(ADV_REG_PAL_COMB_CONTROL)
        new_val = self.__set_bits_in_val(val, mode_bits<<3, 0x7<<3)
        self.__write_reg(ADV_REG_PAL_COMB_CONTROL, new_val)

    def set_chroma_comb_taps(self, taps):
        if taps in ADV_CHROMA_COMB_TAPS.values():
            mode_bits = filter
        elif taps in ADV_CHROMA_COMB_TAPS.keys():
            mode_bits = ADV_CHROMA_COMB_TAPS[taps]
        else:
            return
        val = self.__read_reg(ADV_REG_PAL_COMB_CONTROL)
        new_val = self.__set_bits_in_val(val, mode_bits<<6, 0x3<<6)
        self.__write_reg(ADV_REG_PAL_COMB_CONTROL, new_val)

    def set_CTI(self, is_enabled: bool):
        """
        enables / disables Chroma Transient Improvement
        """
        is_enabled = bool(is_enabled)
        val = self.__read_reg(ADV_REG_CTI_DNR_CONTROL_1)
        new_val = self.__set_bits_in_val(val, is_enabled, 1)
        self.__write_reg(ADV_REG_CTI_DNR_CONTROL_1, new_val)

    def set_alpha_blend(self, level):
        if level in ADV_ALPHA_BLEND_LEVEL.values():
            lvl_bits = filter
        elif level in ADV_ALPHA_BLEND_LEVEL.keys():
            lvl_bits = ADV_ALPHA_BLEND_LEVEL[level]
        else:
            return
        val = self.__read_reg(ADV_REG_CTI_DNR_CONTROL_1)
        new_val = self.__set_bits_in_val(val, lvl_bits<<2, 0x3<<2)
        self.__write_reg(ADV_REG_CTI_DNR_CONTROL_1, new_val)

    def set_noise_reduction(self, is_enabled: bool):
        is_enabled = bool(is_enabled)
        val = self.__read_reg(ADV_REG_CTI_DNR_CONTROL_1)
        new_val = self.__set_bits_in_val(val, is_enabled<<5, 1<<5)
        self.__write_reg(ADV_REG_CTI_DNR_CONTROL_1, new_val)

    def set_CTI_threshold(self, threshold):
        if threshold < 0 or threshold > 255:
            return
        self.__write_reg(ADV_REG_CTI_DNR_CONTROL_2, threshold)

    def set_noise_reduction_threshold(self, threshold):
        if threshold < 0 or threshold > 255:
            return
        self.__write_reg(ADV_REG_DNR_NOISE_THRESHOLD_1, threshold)

    def set_peaking_gain(self, gain):
        if gain < 0 or gain > 255:
            return
        self.__write_reg(ADV_REG_PEAKING_GAIN, gain)

    def __set_bits_in_val(self, val, bits, mask):
        """
        sets bits in a register value according to mask.
        bits and mask have to be shifted to the correct position
        """
        val &= ~(mask)
        val |= bits
        return val

    def __write_reg(self, reg, val, addr=0x21):
        ret = check_output(["i2cset", "-y", "-f", self.i2cbus, hex(addr), hex(reg), hex(val)])
        return ret

    def __read_reg(self, reg, addr=0x21):
        reg_str = check_output(["i2cget", "-y", "-f", self.i2cbus, hex(addr), hex(reg)])
        return int(reg_str.strip(), 16)


if __name__ == '__main__':
    adv = ADV7280()
    #adv.set_luma_comb_mode("Fixed three-line comb")
    #adv.set_chroma_comb_mode("fixed all lines")
    #adv.set_chroma_comb_taps("three taps")

    adv.set_CTI(True)
    adv.set_CTI_threshold(127)

    adv.set_noise_reduction(False)
    adv.set_noise_reduction_threshold(0)

    adv.set_C_shaping_filter("Wideband mode")

    adv.set_alpha_blend("sharpest")
