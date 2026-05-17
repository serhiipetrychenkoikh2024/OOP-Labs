import asyncio
import random
import time
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    # Клас для представлення базового вузла мережі (наприклад, ПК)
    def __init__(self, name):
        self.name = name
        self.connections = [] # Список підключених сусідніх вузлів

    def connect(self, node):
        # Встановлення двостороннього з'єднання між вузлами
        self.connections.append(node)
        node.connections.append(self)

    async def send(self, packet, network):
        # Імітація затримки під час передачі даних
        await asyncio.sleep(random.uniform(0.05, 0.3))

        # Імітація випадкової втрати пакета згідно з налаштуваннями мережі
        if random.random() < network.loss_rate:
            network.packets_lost += 1
            return
        
        # Якщо пакет не втрачено, передаємо його далі
        await self.forward(packet, network)

    async def forward(self, packet, network):
        # Якщо пакет досяг пункту призначення, зупиняємо передачу
        if self == packet.dest:
            return
        
        # Щоб уникнути зациклення, перевіряємо, чи вузол вже обробляв цей пакет
        if self in packet.visited:
            return
        
        # Позначаємо поточний вузол як пройдений
        packet.visited.append(self)

        # Розсилаємо пакет усім підключеним сусідам (широкомовна передача)
        for node in self.connections:
            if node not in packet.visited:
                await node.send(packet, network)

class Router(Node):
    # Клас маршрутизатора успадковує всі властивості звичайного вузла
    pass

class Packet:
    # Клас для зберігання інформації про мережевий пакет
    def __init__(self, src, dest, size, protocol):
        self.src = src           # Відправник
        self.dest = dest         # Отримувач
        self.size = size         # Розмір пакета
        self.protocol = protocol # Тип протоколу (TCP/UDP)
        self.visited = []        # Історія пройдених вузлів

class TCPProtocol:
    name = "TCP"

    @staticmethod
    async def transmit(src, dest, network):
        # Генерація пакета зі специфічним для TCP розміром
        packet = Packet(src, dest, random.randint(200, 500), "TCP")
        await src.send(packet, network)
                        
class UDPProtocol:
    name = "UDP"

    @staticmethod
    async def transmit(src, dest, network):
        # Генерація пакета зі специфічним для UDP розміром
        packet = Packet(src, dest, random.randint(50, 200), "UDP")
        await src.send(packet, network)

class Network:
    # Клас для керування мережею та збору статистики
    def __init__(self):
        self.nodes = []
        self.loss_rate = random.uniform(0.1, 0.15) # Шанс втрати 10-15%
        self.packets_sent = 0
        self.packets_lost = 0
        self.total_time = 0

    async def simulate(self, protocol, packets=5):
        # Запуск симуляції передачі заданої кількості пакетів
        for _ in range(packets):
             # Вибір випадкового відправника та отримувача
             src, dest = random.sample(self.nodes, 2)
             start = time.time()
             self.packets_sent += 1
             await protocol.transmit(src, dest, self)
             self.total_time += time.time() - start

    def analyze(self):
        # Обчислення та виведення статистики мережі
        if self.packets_sent == 0:
            print("Жодного пакета не було відправлено.")
            return

        avg_time = self.total_time / self.packets_sent
        loss = (self.packets_lost / self.packets_sent) * 100
        
        if self.total_time > 0:
            bandwidth = (self.packets_sent - self.packets_lost) / self.total_time
        else:
            bandwidth = 0

        print(f"Середній час передачі: {avg_time:.4f} с")
        print(f"Втрати пакетів: {loss:.2f}%")
        print(f"Пропускна здатність: {bandwidth:.2f} пак/с")

    def visualize(self, title="Топологія мережі"):
        # Побудова графіка мережі за допомогою бібліотеки networkx
        G = nx.Graph()
        for node in self.nodes:
            for conn in node.connections:
                G.add_edge(node.name, conn.name)

        nx.draw(G, with_labels=True, node_color='lightgreen', node_size=2500, font_size=10)
        plt.title(title)
        plt.show()

async def main():
    network = Network()

    # Створення 6 комп'ютерів
    pcs = [Node(f"PC{i}") for i in range(1, 7)]
    network.nodes = pcs

    # Налаштування топології Mesh – кожен комп'ютер з'єднується з усіма іншими
    for i in range(len(pcs)):
        for j in range(i + 1, len(pcs)):
            pcs[i].connect(pcs[j])

    # Запуск симуляції та аналіз
    await network.simulate(TCPProtocol, packets=10)
    network.analyze()
    network.visualize(title="Повнозв'язна сіткова топологія (Mesh)")

if __name__ == "__main__":
    asyncio.run(main())