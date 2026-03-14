"""
Обрано дві топології: Зіркова (Star) та Сіткова (Mesh).

Визначте структуру класів Node, Router для відображення мережевих вузлів.
Додайте методи для встановлення з'єднань між вузлами.

Створіть клас Packet, що міститиме дані про відправника, отримувача, розмір пакета.
Додайте симуляцію випадкової втрати пакетів (10-15% шанс втрати).

Реалізуйте класи TCPProtocol і UDPProtocol, які оброблятимуть пакети відповідно до правил кожного протоколу.

Використайте asyncio для моделювання мережевого трафіку.
Заплануйте події передачі пакетів з випадковими затримками.

Обчисліть статистику для: 
• Часу передачі пакетів
• Кількості втрачених пакетів
• Пропускної здатності мережі

Використайте networkx для створення графічного представлення обраної топології.
Позначте активні зв’язки між вузлами.

Порівняйте результати для різних топологій.
Зробіть висновки про ефективність мережевої топології на основі отриманих даних.
"""
import asyncio
import random
import time
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def connect(self, node):
        self.connections.append(node)
        node.connections.append(self)

    async def send(self, packet, network):
        await asyncio.sleep(random.uniform(0.05, 0.3))

        if random.random() < network.loss_rate:
            network.packets_lost += 1
            return
        
        await self.forward(packet, network)

    async def forward(self, packet, network):
        if self == packet.dest:
            return
        
        if self in packet.visited:
            return
        
        packet.visited.append(self)

        for node in self.connections:
            if node not in packet.visited:
                await node.send(packet, network)

class Router(Node):
    pass

class Packet:
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
        packet = Packet(src, dest, random.randint(200, 500), "TCP")
        await src.send(packet, network)
                        
class UDPProtocol:
    name = "UDP"

    @staticmethod
    async def transmit(src, dest, network):
        packet = Packet(src, dest, random.randint(50, 200), "UDP")
        await src.send(packet, network)

class Network:
    def __init__(self):
        self.nodes = []
        self.loss_rate = random.uniform(0.1, 0.15)
        self.packets_sent = 0
        self.packets_lost = 0
        self.total_time = 0

    async def simulate(self, protocol, packets=5):
        for _ in range(packets):
             src, dest = random.sample(self.nodes, 2)
             start = time.time()
             self.packets_sent += 1
             await protocol.transmit(src, dest, self)
             self.total_time += time.time() - start

    def analyze(self):
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
        G = nx.Graph()
        for node in self.nodes:
            for conn in node.connections:
                G.add_edge(node.name, conn.name)

        nx.draw(G, with_labels=True, node_color='lightgreen', node_size=2500, font_size=10)
        plt.title(title)
        plt.show()

async def main():
    network = Network()

    pcs = [Node(f"PC{i}") for i in range(1, 7)]
    network.nodes = pcs

    for i in range(len(pcs)):
        for j in range(i + 1, len(pcs)):
            pcs[i].connect(pcs[j])

    await network.simulate(TCPProtocol, packets=10)
    network.analyze()
    network.visualize(title="Повнозв'язна сіткова топологія (Mesh)")

if __name__ == "__main__":
    asyncio.run(main())