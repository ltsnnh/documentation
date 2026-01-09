# Clock

### Put HSI clock on MCO (PA8)

After a reset, the STM32F103 defaults to running on its internal HSI.  
SYSCLK source : HSI -> SYSCLK = 8MHz

<p align="center">
    <img src="https://files.catbox.moe/n8rmte.png" width="512"><br>
    Configuration Clock tree HSI - MCO
</p>

[SourceCode](https://github.com/ltsnnh/stm32f103c8t6/tree/master/bare_metal/rcc_hsi_mco)

<p align="center">
    <img src="https://files.catbox.moe/6yevok.jpg" width="512"><br>
    Result HSI - MCO
</p>

### Put HSE clock on MCO (PA8)

<p align="center">
    <img src="https://files.catbox.moe/xixhpn.png" width="512"><br>
    Configuration Clock tree HSE - MCO
</p>

[SourceCode](https://github.com/ltsnnh/stm32f103c8t6/tree/master/bare_metal/rcc_hse_mco)

<p align="center">
    <img src="https://files.catbox.moe/jhzvw6.JPG" width="512"><br>
    Result HSE - MCO
</p>

### Put PLL / 2 clock on MCO (PA8)

<p align="center">
    <img src="https://files.catbox.moe/qjtcnd.png" width="512"><br>
    Configuration Clock tree PLL / 2 - MCO
</p>

[SourceCode](https://github.com/ltsnnh/stm32f103c8t6/tree/master/bare_metal/rcc_pll2_mco)

<p align="center">
    <img src="https://files.catbox.moe/p9fuoy.jpg" width="512"><br>
    Result PLL / 2 - MCO
</p>
