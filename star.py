import asyncio
import random
import time
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    # Клас для представлення базового вузла мережі
    def __init__(self, name):
        self.name = name
        self.connections = []

    def connect(self, node):
        # Встановлення двостороннього з'єднання
        self.connections.append(node)
        node.connections.append(self)

    async def send(self, packet, network):
        # Затримка при передачі пакета
        await asyncio.sleep(random.uniform(0.05, 0.3))

        # Симуляція втрати пакета
        if random.random() < network.loss_rate:
            network.packets_lost += 1
            return
        
        # Пересилка пакета далі
        await self.forward(packet, network)

    async def forward(self, packet, network):
        # Перевірка, чи досягнуто кінцевого адресата
        if self == packet.dest:
            return
        
        # Перевірка на зациклення
        if self in packet.visited:
            return
        
        packet.visited.append(self)

        # Відправка всім сусідам
        for node in self.connections:
            if node not in packet.visited:
                await node.send(packet, network)

class Router(Node):
    # У зірковій топології цей вузол виступає центральним хабом
    pass

class Packet:
    # Дані мережевого пакета
    def __init__(self, src, dest, size, protocol):
        self.src = src
        self.dest = dest
        self.size = size
        self.protocol = protocol
        self.visited = []

class TCPProtocol:
    name = "TCP"

    @staticmethod
    async def transmit(src, dest, network):
        # TCP-пакет має більший розмір
        packet = Packet(src, dest, random.randint(200, 500), "TCP")
        await src.send(packet, network)
                        
class UDPProtocol:
    name = "UDP"

    @staticmethod
    async def transmit(src, dest, network):
        # UDP-пакет є меншим за розміром
        packet = Packet(src, dest, random.randint(50, 200), "UDP")
        await src.send(packet, network)

class Network:
    # Керування мережею та обчислення статистики
    def __init__(self):
        self.nodes = []
        self.loss_rate = random.uniform(0.1, 0.15)
        self.packets_sent = 0
        self.packets_lost = 0
        self.total_time = 0

    async def simulate(self, protocol, packets=5):
        # Симуляція відправки пакетів між випадковими вузлами
        for _ in range(packets):
             src, dest = random.sample(self.nodes, 2)
             start = time.time()
             self.packets_sent += 1
             await protocol.transmit(src, dest, self)
             self.total_time += time.time() - start

    def analyze(self):
        # Звіт про продуктивність мережі
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

    def visualize(self):
        # Відображення структури мережі на графіку
        G = nx.Graph()
        for node in self.nodes:
            for conn in node.connections:
                G.add_edge(node.name, conn.name)

        nx.draw(G, with_labels=True, node_color='lightblue', node_size=2500, font_size=10)
        plt.title("Зіркова топологія")
        plt.show()

async def main():
    network = Network()

    # Створення центрального маршрутизатора та 4 комп'ютерів
    router = Router("Router")
    pcs = [Node(f"PC{i}") for i in range(1, 5)]
    network.nodes = [router] + pcs

    # Налаштування топології Star – кожен ПК підключається ТІЛЬКИ до маршрутизатора
    for pc in pcs:
        router.connect(pc)

    # Запуск симуляції та аналіз
    await network.simulate(TCPProtocol)
    network.analyze()
    network.visualize()

if __name__ == "__main__":
    asyncio.run(main())