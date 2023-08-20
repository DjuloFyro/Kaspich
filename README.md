<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!--<a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>-->

  <h1 align="center">Kaspich - Chess AI Engine</h1>
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
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Kaspich is an AI Engine.

The game board has been constructed using the bitboard representation, optimizing processing speed.

Several algorithms have been employed within the AI, with the most efficient being the Negamax Beta Pruning. This algorithm is utilized for games against the AI.

You can engage in gameplay using a GUI built with Pygame.
In the "IA VS IA" section, a random algorithm is pitted against the Negamax algorithm.
In the "PLAYER VS IA" section, you can challenge the AI using the Negamax algorithm.

### Built With

![Py][Python]

## Getting Started
### Prerequisites

You need ``numpy`` and ``pygame`` installed


<!-- USAGE EXAMPLES -->
## Usage

You can run the `src/game_gui.py` to launch the final game:
```sh
python src/game_gui.py
```



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- CONTACT -->
## Contact

Julian Gil - juliangil2424@gmail.com

<!-- MARKDOWN LINKS & IMAGES -->
[Python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python&logoColor=white
