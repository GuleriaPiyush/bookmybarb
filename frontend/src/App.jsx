import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [backendConnected, setBackendConnected] = useState(false)
  
  // Interactive Booking State
  const [selectedServices, setSelectedServices] = useState([])
  const [activeCategory, setActiveCategory] = useState('All')
  const [selectedBarber, setSelectedBarber] = useState('')
  const [bookingDate, setBookingDate] = useState('')
  const [bookingTime, setBookingTime] = useState('')
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [bookingConfirmed, setBookingConfirmed] = useState(false)

  // Barber list
  const barbers = [
    { id: 1, name: "Marcus 'Blade' Vance", role: "Master Barber", rating: "4.9", avatar: "🧔" },
    { id: 2, name: "Sophia Martinez", role: "Artistic Hair Stylist", rating: "4.8", avatar: "👩‍🦰" },
    { id: 3, name: "Alexander Kross", role: "Beard Sculpt Specialist", rating: "5.0", avatar: "🧔‍♂️" }
  ]

  // Fallback offline mock services in case backend is loading or not running
  const mockServices = [
    {
      "id": 1,
      "name": "Classic Gent's Haircut",
      "category": "Haircuts",
      "description": "Tailored cut, hot towel finish, wash, blowdry & premium styling product application.",
      "price": 35.00,
      "duration": "45 mins",
      "popular": true,
      "icon": "✂️"
    },
    {
      "id": 2,
      "name": "Signature Beard Trim & Sculpt",
      "category": "Beard Grooming",
      "description": "Precision beard sculpt with line-up, hot towel treatment, conditioning beard oil & massage.",
      "price": 25.00,
      "duration": "30 mins",
      "popular": true,
      "icon": "🧔"
    },
    {
      "id": 3,
      "name": "Royal Hot Towel Shave",
      "category": "Shaving",
      "description": "Traditional straight razor shave, pre-shave oil, thick lather, ice-cold towel & soothing balm.",
      "price": 40.00,
      "duration": "50 mins",
      "popular": false,
      "icon": "💈"
    },
    {
      "id": 4,
      "name": "The Executive Package",
      "category": "Combos",
      "description": "Classic Haircut, Signature Beard Trim, soothing charcoal face mask, and premium scalp massage.",
      "price": 75.00,
      "duration": "90 mins",
      "popular": true,
      "icon": "⭐"
    }
  ]

  // Fetch from Django Backend
  const fetchServices = () => {
    setLoading(true)
    setError(null)
    
    // Using standard native fetch as requested
    fetch('http://localhost:8000/api/services/')
      .then(response => {
        if (!response.ok) {
          throw new Error(`Server returned status: ${response.status}`)
        }
        return response.json()
      })
      .then(data => {
        if (data && data.data) {
          setServices(data.data)
          setBackendConnected(true)
        } else {
          throw new Error("Invalid response format from Django")
        }
        setLoading(false)
      })
      .catch(err => {
        console.warn("Backend fetch failed, using offline fallback data:", err.message)
        // Fallback gracefully so UI remains extremely premium and fully usable
        setServices(mockServices)
        setBackendConnected(false)
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchServices()
  }, [])

  // Handle service selection
  const toggleService = (service) => {
    if (selectedServices.find(s => s.id === service.id)) {
      setSelectedServices(selectedServices.filter(s => s.id !== service.id))
    } else {
      setSelectedServices([...selectedServices, service])
    }
  }

  // Get unique categories
  const categories = ['All', ...new Set(services.map(s => s.category))]

  // Filter services
  const filteredServices = activeCategory === 'All' 
    ? services 
    : services.filter(s => s.category === activeCategory)

  // Booking calculations
  const subtotal = selectedServices.reduce((sum, s) => sum + s.price, 0)
  const serviceFee = selectedServices.length > 0 ? 3.50 : 0
  const total = subtotal + serviceFee

  const handleBookNow = () => {
    if (selectedServices.length === 0) {
      alert("Please select at least one service.")
      return
    }
    if (!selectedBarber) {
      alert("Please select your preferred stylist.")
      return
    }
    if (!bookingDate || !bookingTime) {
      alert("Please select a date and time slot.")
      return
    }
    setIsModalOpen(true)
  }

  const confirmFinalBooking = () => {
    setBookingConfirmed(true)
    setTimeout(() => {
      // Clear cart on success after some delay
      setSelectedServices([])
      setSelectedBarber('')
      setBookingDate('')
      setBookingTime('')
      setIsModalOpen(false)
      setBookingConfirmed(false)
    }, 4000)
  }

  return (
    <div className="barber-app">
      {/* Premium Header */}
      <header className="barber-header">
        <div className="header-brand">
          <div className="barber-pole-logo">
            <span className="pole-line red"></span>
            <span className="pole-line white"></span>
            <span className="pole-line blue"></span>
          </div>
          <h1>BookMyBarb</h1>
        </div>
        <div className="backend-badge">
          {backendConnected ? (
            <span className="badge connected">
              <span className="dot"></span> Connected to Django API
            </span>
          ) : (
            <span className="badge offline" onClick={fetchServices} title="Click to retry connecting to Django backend">
              <span className="dot"></span> Showing Offline Mode (Click to connect to Django)
            </span>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <section className="barber-hero">
        <div className="hero-content">
          <span className="gold-subtitle">EXQUISITE GROOMING EXPERIENCE</span>
          <h2>Timeless Style & Premium Care</h2>
          <p>
            Experience custom haircuts, precision beard sculpts, and relaxing hot towel treatments from our master craftsmen. 
            Select your desired services and book your reservation below.
          </p>
        </div>
      </section>

      <main className="barber-layout">
        {/* Left Side: Services Directory */}
        <section className="services-section">
          <div className="section-header">
            <h3>Select Services</h3>
            {/* Category Filter Tabs */}
            <div className="category-tabs">
              {categories.map(cat => (
                <button
                  key={cat}
                  className={`tab-btn ${activeCategory === cat ? 'active' : ''}`}
                  onClick={() => setActiveCategory(cat)}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>

          {loading ? (
            <div className="loading-container">
              <div className="spinner"></div>
              <p>Fetching premium services...</p>
            </div>
          ) : (
            <div className="services-grid">
              {filteredServices.map(service => {
                const isSelected = selectedServices.some(s => s.id === service.id)
                return (
                  <div 
                    key={service.id} 
                    className={`service-card ${isSelected ? 'selected' : ''} ${service.popular ? 'popular' : ''}`}
                    onClick={() => toggleService(service)}
                  >
                    {service.popular && <span className="popular-badge">POPULAR</span>}
                    <div className="service-card-header">
                      <span className="service-icon">{service.icon || '✂️'}</span>
                      <span className="service-price">${service.price.toFixed(2)}</span>
                    </div>
                    <h4>{service.name}</h4>
                    <p className="service-description">{service.description}</p>
                    <div className="service-card-footer">
                      <span className="service-duration">⏱️ {service.duration}</span>
                      <button 
                        className={`select-btn ${isSelected ? 'selected' : ''}`}
                        onClick={(e) => {
                          e.stopPropagation()
                          toggleService(service)
                        }}
                      >
                        {isSelected ? '✓ Selected' : 'Add to Reservation'}
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </section>

        {/* Right Side: Interactive Booking Panel */}
        <aside className="booking-sidebar">
          <div className="sidebar-card">
            <h3>Your Reservation</h3>
            
            {/* Selected Items */}
            <div className="selected-services-list">
              {selectedServices.length === 0 ? (
                <div className="empty-cart">
                  <span className="cart-icon">💈</span>
                  <p>No services selected.</p>
                  <p className="subtext">Select one or more services from the list to start building your customized session.</p>
                </div>
              ) : (
                selectedServices.map(s => (
                  <div key={s.id} className="cart-item">
                    <div className="cart-item-info">
                      <span className="cart-item-name">{s.name}</span>
                      <span className="cart-item-duration">{s.duration}</span>
                    </div>
                    <div className="cart-item-actions">
                      <span className="cart-item-price">${s.price.toFixed(2)}</span>
                      <button className="remove-item" onClick={() => toggleService(s)}>×</button>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Barber Selection */}
            {selectedServices.length > 0 && (
              <div className="form-group">
                <label>Select Master Barber</label>
                <div className="barber-select-grid">
                  {barbers.map(b => (
                    <div 
                      key={b.id} 
                      className={`barber-option ${selectedBarber === b.name ? 'active' : ''}`}
                      onClick={() => setSelectedBarber(b.name)}
                    >
                      <span className="barber-avatar">{b.avatar}</span>
                      <div className="barber-info">
                        <span className="barber-name">{b.name}</span>
                        <span className="barber-rating">⭐ {b.rating} - {b.role}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Date and Time Selection */}
            {selectedServices.length > 0 && selectedBarber && (
              <div className="booking-datetime-row">
                <div className="form-group">
                  <label>Select Date</label>
                  <input 
                    type="date" 
                    value={bookingDate} 
                    onChange={(e) => setBookingDate(e.target.value)}
                    min={new Date().toISOString().split('T')[0]}
                    className="datetime-input"
                  />
                </div>
                <div className="form-group">
                  <label>Select Time</label>
                  <select 
                    value={bookingTime} 
                    onChange={(e) => setBookingTime(e.target.value)}
                    className="datetime-input"
                  >
                    <option value="">Choose Time</option>
                    <option value="09:00 AM">09:00 AM</option>
                    <option value="10:30 AM">10:30 AM</option>
                    <option value="12:00 PM">12:00 PM</option>
                    <option value="01:30 PM">01:30 PM</option>
                    <option value="03:00 PM">03:00 PM</option>
                    <option value="04:30 PM">04:30 PM</option>
                    <option value="06:00 PM">06:00 PM</option>
                  </select>
                </div>
              </div>
            )}

            {/* Cost Summary */}
            {selectedServices.length > 0 && (
              <div className="booking-summary-costs">
                <div className="summary-row">
                  <span>Subtotal</span>
                  <span>${subtotal.toFixed(2)}</span>
                </div>
                <div className="summary-row">
                  <span>Grooming Amenity Fee</span>
                  <span>${serviceFee.toFixed(2)}</span>
                </div>
                <div className="summary-row total">
                  <span>Total Amount</span>
                  <span>${total.toFixed(2)}</span>
                </div>
                
                <button className="book-btn" onClick={handleBookNow}>
                  Book Session with {selectedBarber ? selectedBarber.split(' ')[0] : 'Stylist'}
                </button>
              </div>
            )}
          </div>
        </aside>
      </main>

      {/* Confirmation Modal */}
      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content glassmorphism">
            {!bookingConfirmed ? (
              <>
                <span className="modal-close" onClick={() => setIsModalOpen(false)}>×</span>
                <div className="modal-header">
                  <span className="modal-badge">RESERVATION DETAILS</span>
                  <h2>Review Your Booking</h2>
                  <p>Confirm details below to complete your premium reservation.</p>
                </div>

                <div className="receipt">
                  <div className="receipt-header">
                    <h4>BOOKMYBARB LOUNGE</h4>
                    <p>Downtown Executive Suites</p>
                  </div>
                  <div className="receipt-section">
                    <p><strong>Stylist:</strong> {selectedBarber}</p>
                    <p><strong>Date:</strong> {bookingDate}</p>
                    <p><strong>Time:</strong> {bookingTime}</p>
                  </div>
                  <div className="receipt-items">
                    <label>Selected Services</label>
                    {selectedServices.map(s => (
                      <div key={s.id} className="receipt-item">
                        <span>{s.name}</span>
                        <span>${s.price.toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                  <div className="receipt-totals">
                    <div className="receipt-row">
                      <span>Subtotal</span>
                      <span>${subtotal.toFixed(2)}</span>
                    </div>
                    <div className="receipt-row">
                      <span>Amenity Fee</span>
                      <span>${serviceFee.toFixed(2)}</span>
                    </div>
                    <div className="receipt-row total">
                      <span>Total</span>
                      <span>${total.toFixed(2)}</span>
                    </div>
                  </div>
                </div>

                <div className="modal-actions">
                  <button className="cancel-btn" onClick={() => setIsModalOpen(false)}>Modify Booking</button>
                  <button className="confirm-btn animate-pulse" onClick={confirmFinalBooking}>Confirm Reservation</button>
                </div>
              </>
            ) : (
              <div className="booking-success-animation">
                <div className="checkmark-circle">
                  <div className="checkmark draw"></div>
                </div>
                <h2>Session Booked!</h2>
                <p className="success-subtitle">Your appointment has been registered successfully.</p>
                <div className="success-details-card">
                  <p><strong>Barber:</strong> {selectedBarber}</p>
                  <p><strong>Date & Time:</strong> {bookingDate} at {bookingTime}</p>
                  <p>A confirmation SMS & calendar invite has been sent to you.</p>
                </div>
                <div className="success-footer-text">
                  Returning to main screen...
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Luxury Footer */}
      <footer className="barber-footer">
        <p>© 2026 BookMyBarb Lounge. Handcrafted for Gentlemen and Stylists.</p>
        <p className="footer-links">
          <span>Terms of Service</span> | <span>Privacy Policy</span> | <span>Downtown Executive Club</span>
        </p>
      </footer>
    </div>
  )
}

export default App
