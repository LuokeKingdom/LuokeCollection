<p align="center">
<a href="https://github.com/LuokeKingdom/LuokeCollection/projects/1">
<img align="center" src="https://user-images.githubusercontent.com/55712285/178427638-626dd05c-06fc-46ac-83b2-8a76bff98443.png" width="200"/>
</a>
</p>

# LuokeCollection 洛克王國 寵物圖鑑
![Tests](https://github.com/LuokeKingdom/LuokeCollection/actions/workflows/ci.yml/badge.svg)

This project aims to recreate a PET index of the game Roco Kingdom

## In-game Screenshot
![In-game Screenshot](https://user-images.githubusercontent.com/55712285/178428547-2d43b702-726f-4df1-aa74-60519304d84b.png)
## Instructions
* pre-req: poetry make
* find `assets` folder in releases
* extract the `assets` folder to `./assets`
* To run: `make` or `make run`
* To reformat: `make black`
* To check code quality: `make lint`
* To bump the version of the project: `make versoin major/minor/patch` 
* To build the project: `make build`
    * make sure you add pyinstaller's path to system path
    * executable is at `dist/index.exe`
