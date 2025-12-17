# Robot Workcell Simulator
**By: Oluwaseun Ajayi**  
**Date: December 15, 2025**

## Overview
Simulates a 6-axis robot arm moving plates between lab devices in an automated workcell. This project demonstrates the concepts I will use at my J&J co-op for building transport networks between automation systems.

I created this simulator to explore how automation coordinates multiple lab devices efficiently and safely. It allows me to practice controlling robots, tracking plates, and ensuring every step in a workflow is precise and traceable. By modeling real-world constraints, I gained insight into how robots can increase throughput and reduce errors, preparing me for the work I will do at J&J.

## What It Does
- Robot picks plates from storage
- Moves them through a 5-device workflow
- Tracks positions in 3D space
- Manages device states
- Logs all operations for traceability

## Devices
1. **Storage** - Plate storage (100, 200, 50)mm
2. **Liquid Handler** - Adds reagents (400, 200, 100)mm
3. **Centrifuge** - Pellets cells (550, 400, 75)mm
4. **Thermal Cycler** - Incubates samples (700, 200, 80)mm
5. **Plate Reader** - Measures results (1000, 200, 90)mm

## Workflow
The robot executes this 8-step protocol:

1. **Storage** → Pick plate
2. **Liquid Handler** → Add cell culture media and reagents
3. **Centrifuge** → Pellet cells by centrifugation
4. **Thermal Cycler** → Incubate at 37°C
5. **Plate Reader** → Measure absorbance at 450nm
6. **Storage** → Return plate
7. **Home** → Robot returns to start position
8. **Log** → Generate complete protocol execution log

## How to Run
```bash
cd robot_practice
python robot_workcell.py
```
Press Enter when prompted to start the automated protocol.

## Sample Output
```
🤖 RobotArm moving to Storage...
  Distance: 229.1mm | Time: 2.29s
✅ Arrived at Storage
🤏 RobotArm picking plate CELL_CULTURE_PLATE_001...
✅ Plate secured in gripper

📋 PROTOCOL EXECUTION LOG
Time       Plate ID                  From            To              Status
----------------------------------------------------------------------
18:13:18   CELL_CULTURE_PLATE_001    Storage         LiquidHandler   ✅
18:13:24   CELL_CULTURE_PLATE_001    LiquidHandler   Centrifuge      ✅
18:13:28   CELL_CULTURE_PLATE_001    Centrifuge      ThermalCycler   ✅
18:13:35   CELL_CULTURE_PLATE_001    ThermalCycler   PlateReader     ✅
18:13:39   CELL_CULTURE_PLATE_001    PlateReader     Storage         ✅
```

## Key Concepts
✅ 3D coordinate systems and distance calculations  
✅ Robot path planning and movement optimization  
✅ State management (tracking plate locations)  
✅ Error handling (prevents impossible operations)  
✅ Sequential automation workflows  
✅ Protocol logging and traceability  
✅ Object-oriented design patterns  

## Technical Details

### Position Class
Every device has 3D coordinates (x, y, z) in millimeters. The robot calculates Euclidean distance to plan efficient movements:
```python
distance = sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)
```

### State Management
The system tracks:
- Robot position and gripper state
- Device locations and status
- Plate locations at all times
- Operation history and timestamps

### Error Handling
Prevents common automation errors:
- ❌ Picking from empty location
- ❌ Placing in occupied location
- ❌ Processing without a plate
- ❌ Double-picking plates

## Technologies
- **Python 3.x**
- Object-oriented programming
- Math library (distance calculations)
- Datetime (timestamp logging)
- Time module (operation simulation)

## Enhancements Made
✅ Added Centrifuge device to workcell  
✅ Integrated centrifugation step into protocol  
✅ Updated device count from 4 to 5  
✅ Modified workflow to include cell pelleting step  
✅ Debugged and fixed duplicate transfer attempts  
✅ Verified error handling with protocol logs  

## Relevance to J&J Co-op
This simulator directly relates to my upcoming co-op project:

**My Simulator** → **J&J Reality**
- `RobotArm` class → KUKA/Stäubli industrial robots
- `Position(x,y,z)` → Real coordinate systems
- `transfer_plate()` → Mobile robot transport between rooms
- `protocol_log` → Manufacturing batch records (GMP compliance)
- Python automation → Actual workcell control software

The transport network project I'll build will coordinate robots moving materials between workcells in different lab rooms - exactly like this simulation, but at facility scale!

## Skills Demonstrated
✅ Object-oriented programming (classes, inheritance)  
✅ 3D coordinate geometry and calculations  
✅ State machine design  
✅ Error handling and validation  
✅ Protocol automation and sequencing  
✅ Logging and traceability systems  
✅ Code documentation and commenting  
✅ Real-world debugging from logs  

## Future Enhancements
Ideas for further development:
- Add parallel processing (multiple plates simultaneously)
- Implement collision detection
- Add visualization of robot movements
- Integrate with API systems for device control
- Add more devices (incubators, washers, sealers)
- Implement scheduling algorithms for optimal throughput
- Add real-time monitoring dashboard

## Files
- `robot_workcell.py` - Main simulator code (~350 lines)
- `README.md` - This documentation

## What I Learned
This project taught me the fundamentals of:
1. **Robotic coordination** - How robots move and interact with devices
2. **Spatial reasoning** - 3D positioning and path planning
3. **System integration** - Coordinating multiple devices in a workflow
4. **Industrial automation** - Error handling, logging, traceability
5. **Professional development** - Documentation, debugging, iterative improvement

Perfect preparation for my J&J Cell Engineering & Analytical Sciences co-op!

---

*Part of my lab automation practice projects for J&J co-op preparation*  
*See also: API Automation System (plate reader control)*