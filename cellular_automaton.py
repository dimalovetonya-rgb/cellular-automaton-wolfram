import subprocess
import sys

REQUIRED_PACKAGES = ["numpy", "pillow"]

for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
    except ImportError:
        print(f" Библиотека {package} не найдена. Устанавливаю...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f" Библиотека {package} успешно установлена!")

import numpy as np
from PIL import Image


def get_rule_map(rule_number: int) -> dict:

    binary_rule = f"{rule_number:08b}"[::-1]
    rule_map = {}
    for i in range(8):
        triplet = f"{i:03b}"
        rule_map[triplet] = int(binary_rule[i])
    return rule_map

def generate_ca(rule_number: int, width: int, depth: int, initial_state: str = "center") -> np.ndarray:

    rule_map = get_rule_map(rule_number)

    grid = np.zeros((depth, width), dtype=int)

    if initial_state == "center":
        grid[0, width // 2] = 1
    elif initial_state == "random":
        grid[0] = np.random.choice([0, 1], size=width)

    for t in range(1, depth):
        for x in range(width):

            left = grid[t - 1, (x - 1) % width]
            center = grid[t - 1, x]
            right = grid[t - 1, (x + 1) % width]

            triplet = f"{left}{center}{right}"
            grid[t, x] = rule_map[triplet]

    return grid

def analyze_symmetry(grid: np.ndarray) -> str:
    flipped_grid = np.fliplr(grid)
    if np.array_equal(grid, flipped_grid):
        return "Диаграмма абсолютно симметрична относительно вертикальной оси."
    else:
        # Считаем процент совпадающих пикселей для оценки частичной симметрии
        matching_ratio = np.mean(grid == flipped_grid) * 100
        return f"Диаграмма асимметрична. Сходство с зеркальной копией: {matching_ratio:.1f}%."


def save_to_image(grid: np.ndarray, filename: str = "ca_diagram.png", scale: int = 4):

    img_data = (1 - grid) * 255
    img = Image.fromarray(img_data.astype(np.uint8), mode='L')

    new_size = (img.width * scale, img.height * scale)
    img = img.resize(new_size, resample=Image.NEAREST)
    img.save(filename)
    print(f" Изображение успешно сохранено как: {filename}")

if __name__ == "__main__":

    RULE = 30
    WIDTH = 201
    DEPTH = 100
    INIT_MODE = "center"

    print(f"--- Генерация Клеточного Автомата (Правило {RULE}) ---")

    diagram = generate_ca(rule_number=RULE, width=WIDTH, depth=DEPTH, initial_state=INIT_MODE)

    symmetry_result = analyze_symmetry(diagram)
    print(f"Анализ симметрии: {symmetry_result}")

    save_to_image(diagram, filename=f"rule_{RULE}_diagram.png", scale=4)
