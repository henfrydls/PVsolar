# PVsolar

<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/henfrydls/PVsolar">
    <img src="https://github.com/henfrydls/PVsolar/blob/main/Images/logo.ico" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">PVsolar</h3>

  <p align="center">
    A graphical user interface (GUI) able to help distribute solar panels into an inverter MPPT inputs and estimate amount of solar panels needed to supply a user demand based on location.
    <br />
    <a href="#getting-started">Installation</a>
    ·
    <a href="https://github.com/henfrydls/PVsolar/issues">Report Bug</a>
    ·
    <a href="https://github.com/henfrydls/PVsolar/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This program is oriented toward photovoltaic power generation systems. In photovoltaic systems energy is firstly obtained in DC and, to convert it to the same type of energy we received from the grid, we need to use inverters.

There are three types of solar inverters available. 

These types are:
* String inverters 
* Power optimizers + inverter
* Microinverters. 

This program is focused on string inverters. In this type of inverter, solar panels are distributed on what's known as a Maximum Power Point Tracker (MPPT). As the distribution of photovoltaic panels increases, the distribution becomes more complicated.

This program aims to help efficiency in the distribution of solar panels in inverters (MPPT).

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Tkinter](https://docs.python.org/3/library/tkinter.html)
* [Pillow](https://pillow.readthedocs.io/en/stable/)
* [pandas](https://pandas.pydata.org/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [urllib](https://docs.python.org/3/library/urllib.html)
* [OpenCageGeocode](https://opencagedata.com/)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Make sure your Python version is Python 3.7 or above. Run the following command to confirm

  ```sh
  python --version
  ```

### Installation

_Here is an example of how you can install and run this app._

1. Clone the repo
   ```sh
   git clone https://github.com/henfrydls/PVsolar.git
   ```
2. Install required libraries `requirements.txt`
   ```sh
   pip install -r requirements.txt
   ```
3. Run the app
   ```py
   python visual.py
   ```

<p align="right">(<a href="#top">back to top</a>)</p>


<div id="usage"></div>

<!-- USAGE EXAMPLES -->
## Usage Examples

Let's suppose you have the following configuration:

* 1 string type inverter: Canadian Solar Comercial inverter 75kW (8 MPPT, 16 inputs) [CSI-75K-T480GL02-U](https://static.csisolar.com/wp-content/uploads/sites/3/2021/12/06114422/CanadianSolar_Inverter_3ph_75-100KW-NA_V1.6_June-2021.pdf)
* 160 Solar panels: Canadian Solar 590Wp [HiKu6 Mono 590W](https://www.canadiansolar.com/wp-content/uploads/2020/06/Canadian_Solar-Flyer-HiKu6_CS6Y-MS_EN.pdf)

Notice that this configuration keeps our DC/AC ratio to 1.259. _Learn more about DC/AC ratio here [Ideal Ratio](https://www.solarpowerworldonline.com/2016/07/solar-inverters-clipping-dcac-inverter-load-ratio-ideal/)_

A String is a certain amount of solar modules connected in series. It's important to know our maximum string size based on our inverters, solar panels, locations, etc. Hopefully, most PV sizing software nowadays includes this calculation [How to Calculate PV String Size](https://www.mayfield.energy/blog/pv-string-size)

<div align="center">

![image](https://user-images.githubusercontent.com/78233072/163701020-691acd92-7659-495a-9ee3-c82aa3aa4e0b.png)

  </div>
  
The maximum number of modules is **18 modules** in series *based on a certain location*

After all previous data is determined the question is **"How can I optimize my energy generation?"** and here is where ***PVsolar*** comes into action. 

<div align="center">

![image](https://user-images.githubusercontent.com/78233072/163701517-82a33cb8-d48c-474b-ac5e-093d5ae23d57.png)

  </div>
  
Just fill in the required information and *PVsolar* will give you the best matches for your case of study. 

<div align="center">
  
![image](https://user-images.githubusercontent.com/78233072/163701585-efef2f22-c4cb-4262-9767-12796bc9da35.png)

  </div>
  
The app will always prioritize the best result. In this case, your best match will be to wire 7 strings consisting of 18 modules in series and 2 strings of 17 modules. 

In case you need more configurations, the app will always give you all matches found on the specified intervals.

This type of MPPT distribution as of now is not available in most software destinated for Photovoltaic systems, although some of them can include some features of it. I hope to see most software coming with this feature shortly. 


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](https://github.com/henfrydls/PVsolar/blob/main/LICENSE) for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Henfry De Los Santos - henfry@protonmail.com - henfry.delossantos@gmail.com

Project Link: [https://github.com/henfrydls/PVsolar](https://github.com/henfrydls/PVsolar)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

<div>Iconos diseñados por <a href="https://www.flaticon.es/autores/srip" title="srip">srip
</a> from <a href="https://www.flaticon.es/" title="Flaticon">www.flaticon.es</a></div>
