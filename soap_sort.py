import math
import random
from typing import List, Optional


def is_sorted(arr: List[int]) -> bool:
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def time_to_move_one_unit(v: float, a: float) -> float:
    """计算匀减速运动走完1单位距离的时间"""
    if abs(a) < 1e-8:
        return 1.0 / abs(v) if abs(v) > 1e-8 else float('inf')
    # 计算判别式
    D = v**2 + 2 * a * (-1)
    if D < 0:
        return float('inf')  # 无法到达1格距离
    t1 = (-v + math.sqrt(D)) / a
    t2 = (-v - math.sqrt(D)) / a
    # 选择大于0的解（因为我们需要正时间）
    if t1 > 0:
        return t1
    if t2 > 0:
        return t2
    return float('inf')  # 如果没有正解，返回无穷大


def soap_sort(
    array: List[int],
    energy: Optional[float] = None,
    beta: Optional[float] = None,
    threshold: Optional[float] = None,
) -> List[int]:
    if energy is None:
        energy = len(array)
    if beta is None:
        beta = 0.1
    if threshold is None:
        threshold = 0.01

    n = len(array)

    while not is_sorted(array):
        person_index = random.randint(0, n - 1)
        if person_index == 0:
            soap_index = 1
        elif person_index == n - 1:
            soap_index = n - 2
        else:
            soap_index = random.choice([person_index - 1, person_index + 1])

        person_weight = array[person_index]
        soap_weight = array[soap_index]

        # 方向向量：+1 或 -1
        direction = 1 if soap_index > person_index else -1

        # 初速度（动量守恒）
        v_person = math.sqrt(2 * energy * soap_weight / (person_weight * (person_weight + soap_weight))) * direction
        v_soap = -math.sqrt(2 * energy * person_weight / (soap_weight * (person_weight + soap_weight))) * direction

        a_person = -beta * direction
        a_soap = beta * direction  # 注意反方向

        x_person = float(person_index)
        x_soap = float(soap_index)

        prev_person_index = person_index
        prev_soap_index = soap_index

        while abs(v_person) > threshold or abs(v_soap) > threshold:
            # 匀减速运动走完1格的时间
            t1 = time_to_move_one_unit(v_person, a_person)
            t2 = time_to_move_one_unit(v_soap, a_soap)
            
            # 防止无限循环，如果两个时间都是无穷大，则退出循环
            if math.isinf(t1) and math.isinf(t2):
                v_person = 0
                v_soap = 0
                break
                
            dt = min(t1, t2)
            
            # 检查dt是否为有效值
            if math.isnan(dt) or math.isinf(dt):
                v_person = 0
                v_soap = 0
                break

            # 更新位置和速度
            x_person += v_person * dt + 0.5 * a_person * dt * dt
            x_soap += v_soap * dt + 0.5 * a_soap * dt * dt

            v_person += a_person * dt
            v_soap += a_soap * dt

            # 边界反弹
            if x_person < 0 or x_person > n - 1:
                v_person = -v_person
                a_person = -a_person
                x_person = min(max(x_person, 0), n - 1)

            if x_soap < 0 or x_soap > n - 1:
                v_soap = -v_soap
                a_soap = -a_soap
                x_soap = min(max(x_soap, 0), n - 1)

            # 是否换格子了？
            new_person_index = int(round(x_person))
            new_soap_index = int(round(x_soap))

            if new_person_index != prev_person_index and 0 <= new_person_index < n:
                array[prev_person_index], array[new_person_index] = array[new_person_index], array[prev_person_index]
                prev_person_index = new_person_index

            if new_soap_index != prev_soap_index and 0 <= new_soap_index < n:
                array[prev_soap_index], array[new_soap_index] = array[new_soap_index], array[prev_soap_index]
                prev_soap_index = new_soap_index

    return array


if __name__ == "__main__":
    arr = [4, 3, 2, 6, 5, 7, 8, 1]
    print("Original:", arr)
    sorted_arr = soap_sort(arr.copy(), energy=100, beta=1, threshold=1)
    print("Sorted:", sorted_arr)
