<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/pasblo/ComsChannelsSim">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">project_title</h3>

  <p align="center">
    project_description
    <br />
    <a href="https://github.com/pasblo/ComsChannelsSim"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/pasblo/ComsChannelsSim">View Demo</a>
    ·
    <a href="https://github.com/pasblo/ComsChannelsSim/issues">Report Bug</a>
    ·
    <a href="https://github.com/pasblo/ComsChannelsSim/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project allows the simulation of different channel elements:
* Channel element: Allows simulating how different attenuations affect the power, probabilities of error, and simulate bit by bit error.
* Modulation element: Allows simulating a modulator or demodulator, supports several modulation techniques, such as X-PSK, X-FSK, QAM and PAM. It can be used to calculate different types of error rates, graph SNR curves and calculating bandwiths.
* Power element: Allows the connection of several elements in cascade to calculate their overall effect on a received signal.

All elements support working in natural units or in logarithmic units, and can be chained toguether to sumilate more complex systems.
The repository does also allow the calculation of some values in the system and the optimization of others.

The project contains some examples using all created functions as reference, and most of the functions in the library are documented on how to use them:
* LibraryTester: A program that allows to test the different fucntions and classes to get used to them. Uncomment the part you want to test.
* SamplesSolutions: A program that shows how to use this library in the real world, uses the problems samples proposed and solves them using this library.

Some samples of different sample codes working:


### Built With

* []()
* []()
* []()



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

The project uses some libraries that need to be installed, you can use the pip installer, go check <a href="https://github.com/pypa/get-pip">this project by pypa</a>, on how to install easily pip.
* scipy
  ```sh
  pip install scipy
  ```
* komm
  ```sh
  pip install komm
  ```
* matplotlib
  ```sh
  pip install matplotlib
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/pasblo/ComsChannelsSim.git
   ```


<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/pasblo/ComsChannelsSim/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email

Project Link: [https://github.com/pasblo/ComsChannelsSim](https://github.com/pasblo/ComsChannelsSim)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* []()
* []()
* []()





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/pablo-rivero-l%C3%A1zaro-961333207/