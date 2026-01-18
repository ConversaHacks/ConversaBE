"""
Seed script to populate the database with sample data matching the frontend mock data.
Run this after setting up the database to get started with demo data.
"""

from app.core.database import SessionLocal, engine, Base
from app.models import Person, Conversation, ActionItem


def seed_database():
    """Seed the database with sample data."""
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(Person).count() > 0:
            print("Database already contains data. Skipping seed.")
            return

        print("Seeding database with sample data...")

        # Create People
        people = [
            Person(
                id="p1",
                name="Sarah Chen",
                role="Product Lead at Orio",
                avatar_color="bg-indigo-200",
                last_met="Jan 16",
                met_count=5,
                interests=["Ethical AI", "Hiking", "Ceramics"],
                context="Met at the Design Systems conference last year. Looking for a co-founder.",
                open_follow_ups=["Send the deck regarding the Q3 proposal", "Intro her to Marcus"]
            ),
            Person(
                id="p2",
                name="David Miller",
                role="Freelance Architect",
                avatar_color="bg-emerald-200",
                last_met="Jan 14",
                met_count=12,
                interests=["Sustainable materials", "Jazz", "Coffee brewing"],
                context="Old college friend. Currently renovating a loft in Brooklyn.",
                open_follow_ups=[]
            ),
            Person(
                id="p3",
                name="Elena Rostova",
                role="Investor",
                avatar_color="bg-orange-200",
                last_met="Jan 12",
                met_count=1,
                interests=["Fintech", "Early stage B2B"],
                context="Briefly introduced by Sarah. Interested in the memory space.",
                open_follow_ups=["Schedule a proper 30-min coffee chat"]
            )
        ]

        for person in people:
            db.add(person)

        db.flush()

        # Create Conversations
        conversations = [
            Conversation(
                id="c1",
                person_id="p1",
                participants=["p1", "p3"],
                title="Q3 Beta Roadmap Review",
                date="Jan 16 • 2:30 PM",
                location="Blue Bottle Coffee",
                summary="Discussed the roadmap for the Q3 beta launch. Sarah is concerned about the onboarding flow but loves the new visual direction.",
                key_points=[
                    "Sarah thinks the sign-up process has too many steps.",
                    "Suggests moving the 'Personalization' screen to after account creation.",
                    "She is available next Tuesday for a design review."
                ],
                full_transcript="Sarah: Thanks for meeting up. I've been looking over the Q3 mocks.\n\nMe: Of course. What are your initial thoughts?\n\nSarah: Visuals are stunning, but I really think we're losing people at step 3. It feels heavy. We should look at how Linear does their onboarding—it's much punchier.\n\nElena: I agree with Sarah on the friction. If we're targeting the prosumer market, every extra click is a drop-off point.\n\nMe: That makes sense. We could move the 'Personalization' screen to after the main dashboard setup.\n\nSarah: Exactly. Let's aim for a Tuesday design review to finalize that change."
            ),
            Conversation(
                id="c2",
                person_id="p2",
                participants=["p2"],
                title="Brooklyn Project & Japan Trip",
                date="Jan 14 • 6:00 PM",
                location="The Jazz Corner",
                summary="Casual catch-up. David is finishing the Brooklyn project next month. Talked about his upcoming trip to Japan.",
                key_points=[
                    "Brooklyn project wraps in Feb.",
                    "He needs recommendation for hotels in Kyoto.",
                    "Mentioned he is taking a break from contracting for 2 months."
                ],
                full_transcript="David: It's been a marathon, man. I'm taking two months off starting March.\n\nMe: Well deserved. You still heading to Japan?\n\nDavid: Yeah, Kyoto for ten days. I haven't booked a place yet though.\n\nMe: I have a list of spots from my last trip. I'll send them over."
            ),
            Conversation(
                id="c3",
                person_id="p3",
                participants=["p3"],
                title="Intro to Invisible AI",
                date="Jan 12 • 10:00 AM",
                location="TechCrunch Disrupt",
                summary="Introductory chat. Elena is looking for AI native apps in the productivity space.",
                key_points=[
                    "Elena invests in Pre-seed/Seed.",
                    "Thesis is around 'invisible AI' interfaces."
                ],
                full_transcript="Elena: I see so many chat bots. I'm looking for things that disappear. AI shouldn't feel like a second person you have to manage; it should feel like an extension of your own capability."
            ),
            Conversation(
                id="c4",
                person_id="p1",
                participants=["p1"],
                title="Design System Migration Sync",
                date="Dec 10 • 11:00 AM",
                location="Virtual Call",
                summary="Initial sync regarding the design system migration. Agreed to use Figma variables.",
                key_points=[
                    "Migrating to variables in Q1.",
                    "Need to audit existing color tokens."
                ],
                full_transcript="Sarah: Variables are going to save us so much time. We need to start with the color tokens first though. It's a mess in the legacy file."
            ),
            Conversation(
                id="c5",
                person_id="p1",
                participants=["p1"],
                title="Coffee & Ceramics",
                date="Nov 24 • 4:00 PM",
                location="Design Conf Mixer",
                summary="First meeting. Connected over shared interest in ceramics and ethical AI.",
                key_points=[
                    "Sarah works at Orio.",
                    "She runs a pottery studio on weekends."
                ],
                full_transcript="Sarah: Oh no way, I just bought a wheel last month! I'm trying to master centering. It's so much harder than it looks."
            )
        ]

        for conversation in conversations:
            db.add(conversation)

        db.flush()

        # Create Action Items
        action_items = [
            ActionItem(id="a1", conversation_id="c1", text="Mock up a shortened onboarding flow", completed=False),
            ActionItem(id="a2", conversation_id="c1", text="Send calendar invite for Tuesday Design Review", completed=False),
            ActionItem(id="a3", conversation_id="c2", text="Send list of Kyoto recommendations", completed=False),
            ActionItem(id="a4", conversation_id="c4", text="Run token audit", completed=True),
            ActionItem(id="a5", conversation_id="c5", text="Connect on LinkedIn", completed=True),
        ]

        for action_item in action_items:
            db.add(action_item)

        db.commit()
        print("✓ Database seeded successfully with sample data!")
        print(f"  - Created {len(people)} people")
        print(f"  - Created {len(conversations)} conversations")
        print(f"  - Created {len(action_items)} action items")

    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
