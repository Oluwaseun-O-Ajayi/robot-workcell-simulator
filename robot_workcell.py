import time
import math
from datetime import datetime

class Position:
    """3D position in workcell (x, y, z in mm)"""
    def __init__(self, x, y, z, name=""):
        self.x = x
        self.y = y
        self.z = z
        self.name = name
    
    def distance_to(self, other):
        """Calculate 3D distance to another position"""
        return math.sqrt(
            (self.x - other.x)**2 + 
            (self.y - other.y)**2 + 
            (self.z - other.z)**2
        )
    
    def __repr__(self):
        return f"{self.name} ({self.x}, {self.y}, {self.z})"


class WorkcellDevice:
    """Base class for workcell devices"""
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.status = 'idle'
        self.has_plate = False
        self.plate_id = None
    
    def load_plate(self, plate_id):
        """Load a plate into this device"""
        if self.has_plate:
            raise Exception(f"❌ {self.name} already has plate {self.plate_id}!")
        
        print(f"  📥 Loading plate {plate_id} into {self.name}...")
        time.sleep(0.3)
        self.has_plate = True
        self.plate_id = plate_id
        self.status = 'loaded'
        return True
    
    def unload_plate(self):
        """Remove plate from device"""
        if not self.has_plate:
            raise Exception(f"❌ {self.name} has no plate to unload!")
        
        plate_id = self.plate_id
        print(f"  📤 Unloading plate {plate_id} from {self.name}...")
        time.sleep(0.3)
        self.has_plate = False
        self.plate_id = None
        self.status = 'idle'
        return plate_id
    
    def process(self, duration=2):
        """Run a process on the loaded plate"""
        if not self.has_plate:
            raise Exception(f"❌ {self.name} has no plate to process!")
        
        print(f"  ⚙️  {self.name} processing plate {self.plate_id}... ({duration}s)")
        self.status = 'processing'
        time.sleep(duration)
        self.status = 'complete'
        print(f"  ✅ {self.name} processing complete!")
        return True


class RobotArm:
    """Simulated 6-axis robot arm for moving plates"""
    def __init__(self, name="RobotArm"):
        self.name = name
        self.current_position = Position(0, 0, 0, "Home")
        self.has_plate = False
        self.plate_id = None
        self.speed = 100
        self.moves_count = 0
    
    def move_to(self, target_position):
        """Move robot to target position"""
        distance = self.current_position.distance_to(target_position)
        travel_time = distance / self.speed
        
        print(f"\n  🤖 {self.name} moving to {target_position.name}...")
        print(f"     Current: ({self.current_position.x}, {self.current_position.y}, {self.current_position.z})")
        print(f"     Target:  ({target_position.x}, {target_position.y}, {target_position.z})")
        print(f"     Distance: {distance:.1f}mm | Time: {travel_time:.2f}s")
        
        time.sleep(min(travel_time, 1)) 
        
        self.current_position = target_position
        self.moves_count += 1
        print(f"  ✅ Arrived at {target_position.name}")
        return True
    
    def pick_plate(self, device, plate_id):
        """Pick up a plate from a device"""
        if self.has_plate:
            raise Exception(f"❌ {self.name} already holding plate {self.plate_id}!")
        
        if not device.has_plate:
            raise Exception(f"❌ {device.name} has no plate to pick!")
        
   
        self.move_to(device.position)
        
 
        print(f"\n  🤏 {self.name} picking plate {plate_id} from {device.name}...")
        time.sleep(0.5)
        
        device.unload_plate()
        self.has_plate = True
        self.plate_id = plate_id
        print(f"  ✅ Plate {plate_id} secured in gripper")
        return True
    
    def place_plate(self, device):
        """Place held plate into a device"""
        if not self.has_plate:
            raise Exception(f"❌ {self.name} not holding a plate!")
        
        if device.has_plate:
            raise Exception(f"❌ {device.name} already has plate {device.plate_id}!")
        
    
        self.move_to(device.position)
        

        print(f"\n  🤲 {self.name} placing plate {self.plate_id} in {device.name}...")
        time.sleep(0.5)
        
        plate_id = self.plate_id
        device.load_plate(plate_id)
        self.has_plate = False
        self.plate_id = None
        print(f"  ✅ Plate {plate_id} placed successfully")
        return True
    
    def return_home(self):
        """Return to home position"""
        home = Position(0, 0, 0, "Home")
        self.move_to(home)
        print(f"  🏠 {self.name} returned to home position\n")


class Workcell:
    """Complete automated workcell system"""
    def __init__(self, name):
        self.name = name
        self.robot = RobotArm()
        self.devices = {}
        self.protocol_log = []
        self.start_time = None
    
    def add_device(self, device):
        """Add a device to the workcell"""
        self.devices[device.name] = device
        print(f"  ➕ Added {device.name} at position {device.position}")
    
    def transfer_plate(self, plate_id, from_device_name, to_device_name):
        """Transfer a plate from one device to another"""
        from_device = self.devices[from_device_name]
        to_device = self.devices[to_device_name]
        
        print("\n" + "─" * 70)
        print(f"📦 TRANSFER: {plate_id}")
        print(f"   From: {from_device_name} → To: {to_device_name}")
        print("─" * 70)
        
        try:
       
            self.robot.pick_plate(from_device, plate_id)
            
         
            self.robot.place_plate(to_device)
            
          
            self.protocol_log.append({
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'plate_id': plate_id,
                'from': from_device_name,
                'to': to_device_name,
                'status': 'success'
            })
            
            print(f"\n✅ Transfer complete: {from_device_name} → {to_device_name}")
            return True
            
        except Exception as e:
            print(f"\n❌ Transfer failed: {e}")
            self.protocol_log.append({
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'plate_id': plate_id,
                'from': from_device_name,
                'to': to_device_name,
                'status': 'failed',
                'error': str(e)
            })
            return False
    
    def run_cell_screening_protocol(self):
        """Run a complete cell line screening protocol"""
        self.start_time = datetime.now()
        
        print("\n" + "=" * 70)
        print(f"🔬 AUTOMATED CELL LINE SCREENING PROTOCOL")
        print(f"   Workcell: {self.name}")
        print(f"   Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        plate_id = "CELL_CULTURE_PLATE_001"
        
        try:
    
            print("\n" + "=" * 70)
            print("STEP 1: Retrieve plate from cold storage")
            print("=" * 70)
            self.transfer_plate(plate_id, "Storage", "LiquidHandler")
            
 
            print("\n" + "=" * 70)
            print("STEP 2: Add cell culture media and reagents")
            print("=" * 70)
            lh = self.devices["LiquidHandler"]
            lh.process(duration=3)

            print("\n" + "=" * 70)
            print("STEP 2.5: Centrifuge to pellet cells")
            print("=" * 70)
            self.transfer_plate(plate_id, "LiquidHandler", "Centrifuge")
            cent = self.devices["Centrifuge"]
            cent.process(duration=2)
            
     
            print("\n" + "=" * 70)
            print("STEP 3: Transfer to thermal cycler for incubation")
            print("=" * 70)
            self.transfer_plate(plate_id, "Centrifuge", "ThermalCycler")
            
     
            print("\n" + "=" * 70)
            print("STEP 4: Incubate at 37°C")
            print("=" * 70)
            tc = self.devices["ThermalCycler"]
            tc.process(duration=4)
            
       
            print("\n" + "=" * 70)
            print("STEP 5: Transfer to plate reader for analysis")
            print("=" * 70)
            self.transfer_plate(plate_id, "ThermalCycler", "PlateReader")
            
 
            print("\n" + "=" * 70)
            print("STEP 6: Read absorbance at 450nm")
            print("=" * 70)
            pr = self.devices["PlateReader"]
            pr.process(duration=2)
            

            print("\n" + "=" * 70)
            print("STEP 7: Return plate to storage")
            print("=" * 70)
            self.transfer_plate(plate_id, "PlateReader", "Storage")
            
   
            print("\n" + "=" * 70)
            print("STEP 8: Robot returning to home position")
            print("=" * 70)
            self.robot.return_home()
            
   
            end_time = datetime.now()
            duration = (end_time - self.start_time).total_seconds()
            
            print("\n" + "=" * 70)
            print("✅ PROTOCOL COMPLETE!")
            print("=" * 70)
            print(f"   End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Duration: {duration:.1f} seconds")
            print(f"   Robot Movements: {self.robot.moves_count}")

            total_transfers = len(self.protocol_log)
            successful_transfers = len([l for l in self.protocol_log if l['status'] == 'success'])
            failed_transfers = total_transfers - successful_transfers
            success_rate = (successful_transfers / total_transfers * 100) if total_transfers > 0 else 0

            print(f"   Total Transfers: {total_transfers}")
            print(f"   Successful: {successful_transfers}")
            print(f"   Failed: {failed_transfers}")
            print(f"   Success Rate: {success_rate:.1f}%")
            print(f"   Est. Distance Traveled: ~{self.robot.moves_count * 400:.0f}mm")
            
           
            self.show_protocol_log()
            
        except Exception as e:
            print(f"\n❌ Protocol failed with error: {e}")
            print("\nPartial log:")
            self.show_protocol_log()
    
    def show_protocol_log(self):
        """Display the protocol execution log"""
        print("\n" + "=" * 70)
        print("📋 PROTOCOL EXECUTION LOG")
        print("=" * 70)
        print(f"{'Time':<10} {'Plate ID':<25} {'From':<15} {'To':<15} {'Status':<10}")
        print("-" * 70)
        
        for entry in self.protocol_log:
            status_icon = "✅" if entry['status'] == 'success' else "❌"
            print(f"{entry['timestamp']:<10} {entry['plate_id']:<25} {entry['from']:<15} {entry['to']:<15} {status_icon}")
        
        print("=" * 70)


def main():
    """Main function to run the workcell simulation"""
    
    print("\n" + "=" * 70)
    print("🤖 ROBOT WORKCELL SIMULATOR")
    print("   Teaching lab automation concepts for J&J co-op")
    print("=" * 70)
    
  
    workcell = Workcell("Cell Line Screening Workcell")
    
    print("\n📍 Setting up workcell devices...")
    print("-" * 70)
    
   
    storage = WorkcellDevice("Storage", Position(100, 200, 50, "Storage"))
    liquid_handler = WorkcellDevice("LiquidHandler", Position(400, 200, 100, "LiquidHandler"))
    thermal_cycler = WorkcellDevice("ThermalCycler", Position(700, 200, 80, "ThermalCycler"))
    plate_reader = WorkcellDevice("PlateReader", Position(1000, 200, 90, "PlateReader"))
    centrifuge = WorkcellDevice("Centrifuge", Position(550, 400, 75, "Centrifuge"))

    storage.has_plate = True
    storage.plate_id = "CELL_CULTURE_PLATE_001"
    print(f"\n  📦 Initial plate location: {storage.name}")
    

    workcell.add_device(storage)
    workcell.add_device(liquid_handler)
    workcell.add_device(thermal_cycler)
    workcell.add_device(plate_reader)
    workcell.add_device(centrifuge)

    print("\n✅ Workcell setup complete!")
    print(f"   Total devices: {len(workcell.devices)}")
    print(f"   Robot position: Home (0, 0, 0)")
    

    input("\n⏸️  Press Enter to start automated protocol...")
    
    workcell.run_cell_screening_protocol()
    
    # Device status summary
    print("\n" + "=" * 70)
    print("📊 FINAL DEVICE STATUS")
    print("=" * 70)
    print(f"{'Device':<20} {'Status':<15} {'Has Plate':<15}")
    print("-" * 70)
    for device_name, device in workcell.devices.items():
        plate_info = f"✅ {device.plate_id}" if device.has_plate else "Empty"
        print(f"{device_name:<20} {device.status:<15} {plate_info}")
        
    print("=" * 70)
    print("\n" + "=" * 70)
    print("🎓 KEY CONCEPTS LEARNED:")
    print("=" * 70)
    print("  1. ✅ Robot coordinate systems and positioning")
    print("  2. ✅ State management (tracking plate locations)")
    print("  3. ✅ Sequential automation workflows")
    print("  4. ✅ Device communication and control")
    print("  5. ✅ Error handling in robotic systems")
    print("  6. ✅ Protocol logging and traceability")
    print("\n💡 This is exactly what you'll program at J&J!")
    print("   Your transport network will coordinate robots moving")
    print("   plates between workcells just like this simulation!")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()