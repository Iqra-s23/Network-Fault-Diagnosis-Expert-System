y
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

# ==========================================
# NETWORK FAULT DIAGNOSIS EXPERT SYSTEM
# Artificial Intelligence Project
# ==========================================

# Knowledge Base: Faults and their solutions
KNOWLEDGE_BASE = {
    "router_power": {
        "name": "Router Power Failure",
        "solution": [
            "Check the router power cable.",
            "Check the power socket.",
            "Restart the router safely."
        ]
    },
    "wifi": {
        "name": "Wi-Fi Connection Problem",
        "solution": [
            "Move closer to the router.",
            "Check Wi-Fi settings.",
            "Restart Wi-Fi on your device."
        ]
    },
    "dns": {
        "name": "DNS Configuration Problem",
        "solution": [
            "Check your DNS settings.",
            "Try another trusted DNS provider.",
            "Restart the network connection."
        ]
    },
    "ip": {
        "name": "IP Address Problem",
        "solution": [
            "Check the device IP configuration.",
            "Reconnect to the network.",
            "Ask the network administrator for help."
        ]
    },
    "isp": {
        "name": "Internet Service Provider Problem",
        "solution": [
            "Check your ISP service status.",
            "Inspect the modem indicator lights.",
            "Contact your internet provider."
        ]
    },
    "cable": {
        "name": "Network Cable Problem",
        "solution": [
            "Check Ethernet cable connections.",
            "Inspect the cable for damage.",
            "Try a known working cable."
        ]
    },
    "unknown": {
        "name": "Unknown Network Fault",
        "solution": [
            "Restart the device and router.",
            "Check network settings.",
            "Contact a network technician if the issue continues."
        ]
    }
}

# Rule-based inference engine
def diagnose(symptoms):
    scores = {
        "router_power": 0,
        "wifi": 0,
        "dns": 0,
        "ip": 0,
        "isp": 0,
        "cable": 0
    }

    # IF-THEN rules
    if symptoms["router_off"]:
        scores["router_power"] += 5

    if symptoms["wifi_weak"]:
        scores["wifi"] += 4

    if symptoms["wifi_connected"] and symptoms["no_internet"]:
        scores["dns"] += 2
        scores["isp"] += 2

    if symptoms["ip_problem"]:
        scores["ip"] += 5

    if symptoms["all_devices"]:
        scores["isp"] += 3

    if symptoms["one_device"]:
        scores["wifi"] += 1
        scores["ip"] += 1

    if symptoms["cable_problem"]:
        scores["cable"] += 5

    if symptoms["router_on"] and symptoms["no_internet"]:
        scores["isp"] += 1

    best_fault = max(scores, key=scores.get)

    if scores[best_fault] == 0:
        best_fault = "unknown"

    return best_fault, scores


def ask_yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter y or n.")


def collect_symptoms():
    print("\n" + "=" * 48)
    print("       NETWORK FAULT DIAGNOSIS SYSTEM")
    print("=" * 48)
    print("Answer the questions about your network.\n")

    symptoms = {}

    symptoms["router_off"] = ask_yes_no(
        "1. Is the router powered off?"
    )

    symptoms["router_on"] = not symptoms["router_off"]

    symptoms["wifi_connected"] = ask_yes_no(
        "2. Is your device connected to Wi-Fi?"
    )

    symptoms["no_internet"] = ask_yes_no(
        "3. Is the internet not working?"
    )

    symptoms["wifi_weak"] = ask_yes_no(
        "4. Is the Wi-Fi signal weak?"
    )

    symptoms["ip_problem"] = ask_yes_no(
        "5. Is an IP address error displayed?"
    )

    symptoms["all_devices"] = ask_yes_no(
        "6. Are all devices unable to access the internet?"
    )

    symptoms["one_device"] = ask_yes_no(
        "7. Is the problem affecting only one device?"
    )

    symptoms["cable_problem"] = ask_yes_no(
        "8. Is an Ethernet cable loose or damaged?"
    )

    return symptoms


def display_results(fault, scores):
    info = KNOWLEDGE_BASE[fault]

    print("\n" + "=" * 48)
    print("             DIAGNOSIS REPORT")
    print("=" * 48)

    print("Date:", datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("Possible fault:", info["name"])

    print("\nRecommended troubleshooting steps:")

    for number, solution in enumerate(info["solution"], start=1):
        print(f"{number}. {solution}")

    print("\nRule scores (not probabilities):")

    for key, score in scores.items():
        print(f"{KNOWLEDGE_BASE[key]['name']}: {score}")

    print("\nNote: This is an educational rule-based system.")
    print("The diagnosis is a suggestion, not a guarantee.")


# Create network topology graph
def draw_network_graph(fault):
    graph = nx.Graph()

    edges = [
        ("Internet", "Router"),
        ("Router", "Switch"),
        ("Router", "Wi-Fi"),
        ("Switch", "Computer"),
        ("Switch", "Server"),
        ("Wi-Fi", "Laptop"),
        ("Wi-Fi", "Mobile")
    ]

    graph.add_edges_from(edges)

    fault_nodes = {
        "router_power": ["Router"],
        "wifi": ["Wi-Fi", "Laptop", "Mobile"],
        "dns": ["Computer", "Laptop", "Mobile"],
        "ip": ["Computer", "Laptop"],
        "isp": ["Internet"],
        "cable": ["Switch", "Computer"],
        "unknown": []
    }

    highlighted = fault_nodes.get(fault, [])

    colors = []

    for node in graph.nodes():
        if node in highlighted:
            colors.append("tomato")
        else:
            colors.append("lightblue")

    plt.figure(figsize=(11, 7))

    position = nx.spring_layout(graph, seed=42)

    nx.draw_networkx(
        graph,
        position,
        with_labels=True,
        node_color=colors,
        node_size=2600,
        font_size=10,
        font_weight="bold",
        edge_color="gray",
        width=2
    )

    plt.title(
        "Network Topology - Possible Fault Highlighted",
        fontsize=14
    )

    plt.axis("off")
    plt.tight_layout()
    plt.savefig("network_topology.png", dpi=200)
    print("\nNetwork graph saved as network_topology.png")
    plt.show()


# Draw a bar chart of rule scores
def draw_score_chart(scores):
    labels = [
        KNOWLEDGE_BASE[key]["name"]
        for key in scores
    ]

    values = list(scores.values())

    plt.figure(figsize=(11, 6))

    bars = plt.barh(labels, values, color="steelblue")

    plt.xlabel("Rule Score")
    plt.title("Network Fault Diagnosis Score Chart")
    plt.grid(axis="x", linestyle="--", alpha=0.4)

    for bar, score in zip(bars, values):
        plt.text(
            score + 0.05,
            bar.get_y() + bar.get_height() / 2,
            str(score),
            va="center"
        )

    plt.tight_layout()
    plt.savefig("diagnosis_chart.png", dpi=200)
    print("Score chart saved as diagnosis_chart.png")
    plt.show()


def save_report(fault, scores):
    filename = "diagnosis_report.txt"
    info = KNOWLEDGE_BASE[fault]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("NETWORK FAULT DIAGNOSIS REPORT\n")
        file.write("=" * 40 + "\n")
        file.write(
            "Generated: "
            + datetime.now().strftime("%Y-%m-%d %H:%M")
            + "\n"
        )
        file.write("Possible fault: " + info["name"] + "\n\n")
        file.write("Recommended solutions:\n")

        for step in info["solution"]:
            file.write("- " + step + "\n")

        file.write("\nRule scores:\n")

        for key, score in scores.items():
            file.write(
                KNOWLEDGE_BASE[key]["name"] + ": " + str(score) + "\n"
            )

        file.write(
            "\nEducational guidance only; verify the fault before acting.\n"
        )

    print("Report saved as", filename)


def main():
    while True:
        symptoms = collect_symptoms()

        fault, scores = diagnose(symptoms)

        display_results(fault, scores)
        save_report(fault, scores)

        draw_network_graph(fault)
        draw_score_chart(scores)

        again = input(
            "\nDiagnose another network problem? (y/n): "
        ).strip().lower()

        if again not in ("y", "yes"):
            print("\nThank you for using the Expert System!")
            break


if __name__ == "__main__":
    main()