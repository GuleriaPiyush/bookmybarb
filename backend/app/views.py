from django.http import JsonResponse

def api_services(request):
    """
    Returns list of premium barber services available for booking at BookMyBarb.
    """
    services = [
        {
            "id": 1,
            "name": "Classic Gent's Haircut",
            "category": "Haircuts",
            "description": "Tailored cut, hot towel finish, wash, blowdry & premium styling product application.",
            "price": 35.00,
            "duration": "45 mins",
            "popular": True,
            "icon": "✂️"
        },
        {
            "id": 2,
            "name": "Signature Beard Trim & Sculpt",
            "category": "Beard Grooming",
            "description": "Precision beard sculpt with line-up, hot towel treatment, conditioning beard oil & massage.",
            "price": 25.00,
            "duration": "30 mins",
            "popular": True,
            "icon": "🧔"
        },
        {
            "id": 3,
            "name": "Royal Hot Towel Shave",
            "category": "Shaving",
            "description": "Traditional straight razor shave, pre-shave oil, thick lather, ice-cold towel & soothing balm.",
            "price": 40.00,
            "duration": "50 mins",
            "popular": False,
            "icon": "💈"
        },
        {
            "id": 4,
            "name": "The Executive Package",
            "category": "Combos",
            "description": "Classic Haircut, Signature Beard Trim, soothing charcoal face mask, and premium scalp massage.",
            "price": 75.00,
            "duration": "90 mins",
            "popular": True,
            "icon": "⭐"
        },
        {
            "id": 5,
            "name": "Express Line-Up",
            "category": "Haircuts",
            "description": "Quick clean up of sideburns, neck line, and fringe to keep you looking sharp between cuts.",
            "price": 15.00,
            "duration": "15 mins",
            "popular": False,
            "icon": "⚡"
        },
        {
            "id": 6,
            "name": "Deep Cleanse Charcoal Mask",
            "category": "Treatments",
            "description": "Exfoliating wash followed by a peel-off active charcoal mask to revitalize skin and remove pores.",
            "price": 20.00,
            "duration": "25 mins",
            "popular": False,
            "icon": "✨"
        }
    ]
    return JsonResponse({
        "status": "success",
        "salon_name": "BookMyBarb - Exclusive Lounge",
        "location": "Downtown Premium Square",
        "results": len(services),
        "data": services
    })
