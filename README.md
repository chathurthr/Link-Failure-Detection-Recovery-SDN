# Link Failure Detection and Recovery using POX Controller in SDN

## 📌 Project Overview

Traditional networks often require manual intervention when a link fails, causing delay in recovery and reduced reliability.
Software Defined Networking (SDN) solves this by separating the control plane from the data plane, enabling centralized control and dynamic routing updates.

This project demonstrates **Link Failure Detection and Recovery** using:

* **POX Controller**
* **Mininet Network Emulator**
* **OpenFlow Protocol**
* **Python**

The controller monitors topology changes, detects failed links, updates flow rules, and restores connectivity through an alternate path.

---

## 🎯 Objectives

* Monitor topology changes dynamically
* Detect link failures between switches
* Update forwarding rules automatically
* Restore connectivity using backup routes
* Demonstrate centralized SDN control

---

## 🛠 Technologies Used

| Tool         | Purpose                         |
| ------------ | ------------------------------- |
| POX          | SDN Controller                  |
| Mininet      | Network Emulation               |
| Open vSwitch | Virtual Switching               |
| Python       | Controller Logic                |
| OpenFlow 1.0 | Controller-Switch Communication |

---

## 🌐 Network Topology

```text
        h1
         |
        s1 ------- s2 ------- h2
         \         /
          \       /
             s3
```

### Components

* Hosts: `h1`, `h2`
* Switches: `s1`, `s2`, `s3`

### Available Paths

Primary Path:

```text
h1 → s1 → s2 → h2
```

Backup Path:

```text
h1 → s1 → s3 → s2 → h2
```

---

## 📁 Project Files

```text
README.md
topology.py
link_failure.py
screenshots/
logs/
```

### File Description

* `topology.py` → Creates Mininet custom topology
* `link_failure.py` → Custom POX controller logic
* `screenshots/` → Proof of execution
* `logs/` → Terminal outputs

---

## ⚙️ Execution Steps

### Step 1: Clean Previous Sessions

```bash
sudo mn -c
pkill -f pox.py
```

### Step 2: Start POX Controller

```bash
cd ~/pox
python3 pox.py log.level --DEBUG link_failure
```

### Step 3: Start Mininet Topology

```bash
sudo mn --custom ~/topology.py --topo failtopo --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk
```

---

## 🧪 Testing Scenarios

### Scenario 1: Normal Connectivity

```bash
pingall
```

Expected Output:

```text
0% dropped
```

---

### Scenario 2: Simulate Link Failure

```bash
link s1 s2 down
pingall
```

Expected Output:

```text
0% dropped
```

Traffic reroutes through alternate path:

```text
s1 → s3 → s2
```

---

### Scenario 3: Restore Link

```bash
link s1 s2 up
pingall
```

Expected Output:

```text
0% dropped
```

---

## 📊 Results

| Scenario       | Result                  |
| -------------- | ----------------------- |
| Normal Network | Success                 |
| Link Failure   | Connectivity Maintained |
| Link Recovery  | Success                 |

---

## 🔍 Features Implemented

✅ Topology Monitoring
✅ Link Failure Detection
✅ Flow Rule Updates
✅ Alternate Path Recovery
✅ Dynamic SDN Control

---

## Explanation

This project uses a custom POX controller to monitor network topology and detect failures.
When the main link between switches fails, stale flow entries are cleared and traffic is rerouted through an alternate path, maintaining uninterrupted communication.

---

## 📸 Suggested Screenshots

* Controller startup logs
* Switch connection logs
* Normal `pingall` result
* Link failure command
* Ping after failure
* Link recovery command
* Final success result

---

## 🚀 Future Enhancements

* Shortest path routing using Dijkstra algorithm
* Multiple simultaneous failure handling
* Real-time monitoring dashboard
* Email alerts on failure
* Performance analytics

---

## 👨‍💻 Author

CHATHURTH R

---

## 📌 Final Conclusion

This project successfully demonstrates how SDN improves reliability by dynamically detecting failures and restoring connectivity using centralized controller logic.
