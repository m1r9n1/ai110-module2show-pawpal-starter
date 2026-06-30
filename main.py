from datetime import date
from pawpal_system import Owner, Pet, Task

today = date.today()

# --- Owner ---
owner = Owner(
    name="Marina",
    email="marina@example.com",
    phone="555-1234",
    available_minutes_per_day=120,
)

# --- Pets ---
Maki = Pet(id="p1", name="Maki", species="Dog", breed="Dachshund", age=3)
Luna = Pet(id="p2", name="Luna", species="Cat", breed="Black", age=5,
            medical_notes="Hyperthyroid — give meds with food")

owner.add_pet(Maki)
owner.add_pet(Luna)

# --- Tasks for Maki ---
Maki.add_task(Task(
    id="t1", title="Morning Walk", description="30-minute neighborhood walk",
    category="walk", pet=Maki,
    priority=1, estimated_minutes=30, preferred_time_of_day="morning",
))
Maki.add_task(Task(
    id="t2", title="Evening Walk", description="15-minute evening stroll",
    category="walk", pet=Maki,
    priority=2, estimated_minutes=15, preferred_time_of_day="evening",
))
Maki.add_task(Task(
    id="t3", title="Lunch Feeding", description="1 cup dry kibble",
    category="feeding", pet=Maki,
    priority=1, estimated_minutes=5, preferred_time_of_day="afternoon",
))

# --- Tasks for Luna ---
Luna.add_task(Task(
    id="t4", title="Thyroid Medication", description="Half-pill crushed into wet food",
    category="meds", pet=Luna,
    priority=1, estimated_minutes=10, preferred_time_of_day="morning",
))
Luna.add_task(Task(
    id="t5", title="Playtime", description="Interactive feather-wand session",
    category="enrichment", pet=Luna,
    priority=3, estimated_minutes=20, preferred_time_of_day="evening",
))

# --- Generate plan ---
schedule = owner.generate_daily_plan(today)

# --- Print Today's Schedule ---
print("=" * 44)
print("       PAWPAL - TODAY'S SCHEDULE")
print(f"       {today.strftime('%A, %B %d %Y')}")
print("=" * 44)

tasks_today = schedule.get_tasks_for_day(today)

if not tasks_today:
    print("  No tasks scheduled for today.")
else:
    current_time = None
    for task in tasks_today:
        slot = task.preferred_time_of_day.capitalize() if task.preferred_time_of_day else "Anytime"
        if slot != current_time:
            print(f"\n  [{slot}]")
            current_time = slot
        status = "[x]" if task.is_completed else "[ ]"
        print(f"    {status}  {task.pet.name}: {task.title}  (~{task.estimated_minutes} min)")

print()
print("--- Plan Rationale ---")
print(schedule.get_plan_rationale())
print("=" * 44)
