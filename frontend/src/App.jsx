import { useState } from 'react'

function App() {
  const [aiSuggestions, setAiSuggestions] = useState([])
  const [showAISuggestions, setShowAISuggestions] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [tasks, setTasks] = useState([
    { id: 1, task: 'Sample Task 1', completed: false },
    { id: 2, task: 'Sample Task 2', completed: true }
  ])

  const filteredTasks = tasks.filter(task =>
    task.task.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const addTask = () => {
    if (searchQuery.trim()) {
      const newTask = {
        id: Date.now(),
        task: searchQuery,
        completed: false
      }
      setTasks([...tasks, newTask])
      setSearchQuery('')
    }
  }

  const generateAISuggestions = () => {
    const suggestions = [
      "Set a 15-minute timer for focused work sessions",
      "Review and reorganize your tasks by priority",
      "Schedule breaks between major tasks",
      "Create a daily routine checklist",
      "Use the 2-minute rule for quick tasks"
    ]
    setAiSuggestions(suggestions)
    setShowAISuggestions(true)
  }

  return (
    <div className="bg-white min-vh-100">
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideInLeft {
          from { opacity: 0; transform: translateX(-50px); }
          to { opacity: 1; transform: translateX(0); }
        }
        @keyframes slideInRight {
          from { opacity: 0; transform: translateX(50px); }
          to { opacity: 1; transform: translateX(0); }
        }
        @keyframes bounceIn {
          0% { opacity: 0; transform: scale(0.3); }
          50% { opacity: 1; transform: scale(1.05); }
          70% { transform: scale(0.9); }
          100% { opacity: 1; transform: scale(1); }
        }
        body {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          background-attachment: fixed;
          font-family: 'Google Sans', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
          padding-top: 84px;
          color: #fff;
        }
        .hero-section {
          text-align: center;
          padding: 60px 20px;
          animation: fadeIn 1.5s ease-out;
        }
        .hero-title {
          font-size: 3.5rem;
          font-weight: 300;
          margin-bottom: 20px;
          text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
          animation: slideInLeft 1s ease-out 0.5s both;
        }
        .hero-subtitle {
          font-size: 1.25rem;
          margin-bottom: 40px;
          opacity: 0.9;
          animation: slideInRight 1s ease-out 0.7s both;
        }
        .cta-button {
          background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
          border: none;
          color: white;
          padding: 15px 30px;
          font-size: 1.1rem;
          border-radius: 50px;
          cursor: pointer;
          transition: transform 0.3s ease, box-shadow 0.3s ease;
          animation: bounceIn 1s ease-out 1s both;
        }
        .cta-button:hover {
          transform: translateY(-2px);
          box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .search-container {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
        }
        .search-box {
          width: 100%;
          padding: 12px 16px;
          border: 1px solid #dadce0;
          border-radius: 24px;
          font-size: 16px;
          outline: none;
          box-shadow: 0 1px 6px rgba(32,33,36,.28);
        }
        .search-box:focus {
          border-color: #1a73e8;
          box-shadow: 0 1px 6px rgba(32,33,36,.28), 0 0 0 1px #1a73e8;
        }
        .btn-search {
          background-color: #f8f9fa;
          border: 1px solid #f8f9fa;
          border-radius: 4px;
          color: #3c4043;
          font-size: 14px;
          margin: 11px 4px;
          padding: 0 16px;
          height: 36px;
          min-width: 54px;
          text-align: center;
          cursor: pointer;
          user-select: none;
        }
        .btn-search:hover {
          box-shadow: 0 1px 1px rgba(0,0,0,.1);
          background-color: #f8f9fa;
          border: 1px solid #dadce0;
          color: #202124;
        }
        .task-card {
          border: 1px solid #dadce0;
          border-radius: 8px;
          padding: 16px;
          margin: 8px 0;
          background-color: #fff;
          transition: box-shadow 0.2s;
        }
        .task-card:hover {
          box-shadow: 0 1px 3px rgba(60,64,67,.3);
        }
        .ai-modal {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background-color: rgba(0,0,0,0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
        }
        .ai-modal-content {
          background-color: #fff;
          border-radius: 8px;
          padding: 24px;
          max-width: 400px;
          width: 90%;
          box-shadow: 0 4px 6px rgba(32,33,36,.28);
        }
        .footer {
          background-color: #f8f9fa;
          border-top: 1px solid #e9ecef;
          padding: 20px 0;
          margin-top: 50px;
        }
        .footer-links {
          color: #6c757d;
          text-decoration: none;
          font-size: 14px;
          margin: 0 16px 0 0;
        }
        .footer-links:hover {
          text-decoration: underline;
          color: #495057;
        }
        .menu-text {
          font-size: 14px;
          color: #6c757d;
          margin-bottom: 10px;
        }
        .feature-card {
          border: 1px solid #dadce0;
          border-radius: 8px;
          padding: 16px;
          background-color: #fff;
          width: 250px;
          transition: none; /* no hover */
        }
      `}</style>

      {/* Hero Section */}
      <section className="hero-section">
        <h1 className="hero-title">
          <i className="fas fa-tasks me-3"></i>
          Task Management Made Simple
        </h1>
        <p className="hero-subtitle">
          Organize your tasks efficiently with AI-powered suggestions and smart prioritization
        </p>
        <button className="cta-button" onClick={() => window.location.href = '/todolist/'}>
          <i className="fas fa-rocket me-2"></i>
          Get Started
        </button>
      </section>

      {/* Main Content */}
      <main className="container-fluid">
        <div className="search-container">

          <div className="mb-4">
            <input
              type="text"
              className="search-box mb-3"
              placeholder="Search tasks or add new task..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && addTask()}
              style={{fontSize: '16px'}}
            />
            <div className="d-flex justify-content-center">
              <button className="btn-search" onClick={() => filteredTasks.length > 0 ? null : addTask()}>
                {filteredTasks.length > 0 ? 'Search Tasks' : 'Add Task'}
              </button>
              <button className="btn-search" onClick={generateAISuggestions}>
                Get AI Help
              </button>
            </div>
          </div>

          <div className="row">
            <div className="col-md-8 mx-auto">
              {/* Quick Actions */}
              <div className="task-card">
                <h6 className="mb-3 text-dark">Quick Actions</h6>
                <div className="d-flex flex-wrap gap-2">
                  <a href="/todolist/" className="btn btn-outline-primary btn-sm">View All Tasks</a>
                  <button className="btn btn-outline-success btn-sm" onClick={generateAISuggestions}>
                    <i className="fas fa-robot me-1"></i>
                    Get AI Suggestions
                  </button>
                  <button className="btn btn-outline-info btn-sm" onClick={addTask}>
                    <i className="fas fa-plus me-1"></i>
                    Add New Task
                  </button>
                </div>
              </div>

              {/* Recent Tasks Preview */}
              <div className="task-card">
                <h6 className="mb-3 text-dark">Your Tasks</h6>
                <div className="list-group list-group-flush">
                  {filteredTasks.length > 0 ? (
                    filteredTasks.map(task => (
                      <div key={task.id} className="list-group-item d-flex justify-content-between align-items-center">
                        <span>{task.task}</span>
                        <span className={`badge ${task.completed ? 'bg-success' : 'bg-warning'}`}>
                          {task.completed ? 'Completed' : 'Pending'}
                        </span>
                      </div>
                    ))
                  ) : (
                    <p className="text-muted mb-0">No tasks found. Add a new task above!</p>
                  )}
                </div>
              </div>

              {/* Features */}
              <div className="task-card">
                <h6 className="mb-4 text-dark text-center">
                  <i className="fas fa-star text-primary me-2"></i>
                  Powerful Features
                </h6>
                <div className="d-flex flex-wrap justify-content-center">
                  <div className="feature-card text-center mx-2 mb-3">
                    <i className="fas fa-bolt text-warning fs-1 mb-2"></i>
                    <h6 className="text-dark">Fast Workflow</h6>
                    <p className="small text-muted">Streamlined processes for quick task management</p>
                  </div>
                  <div className="feature-card text-center mx-2 mb-3">
                    <i className="fas fa-mobile-alt text-success fs-1 mb-2"></i>
                    <h6 className="text-dark">Responsive UI</h6>
                    <p className="small text-muted">Works perfectly on all devices and screen sizes</p>
                  </div>
                  <div className="feature-card text-center mx-2 mb-3">
                    <i className="fas fa-feather text-info fs-1 mb-2"></i>
                    <h6 className="text-dark">Lightweight</h6>
                    <p className="small text-muted">Minimal footprint with maximum functionality</p>
                  </div>
                  <div className="feature-card text-center mx-2 mb-3">
                    <i className="fas fa-sync-alt text-primary fs-1 mb-2"></i>
                    <h6 className="text-dark">Live Updates</h6>
                    <p className="small text-muted">Changes save immediately via API with instant UI refresh</p>
                  </div>
                  <div className="feature-card text-center mx-2 mb-3">
                    <i className="fas fa-universal-access text-secondary fs-1 mb-2"></i>
                    <h6 className="text-dark">Accessibility</h6>
                    <p className="small text-muted">Keyboard friendly with ARIA labels for better usability</p>
                  </div>
                  <div className="feature-card text-center mx-2 mb-3">
                    <i className="fas fa-rocket text-danger fs-1 mb-2"></i>
                    <h6 className="text-dark">Simple Deploy</h6>
                    <p className="small text-muted">Easy deployment with minimal configuration</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* AI Suggestions Modal */}
      {showAISuggestions && (
        <div className="ai-modal">
          <div className="ai-modal-content">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0">
                <i className="fas fa-robot text-primary me-2"></i>
                AI Productivity Suggestions
              </h5>
              <button
                className="btn-close"
                onClick={() => setShowAISuggestions(false)}
              ></button>
            </div>
            <p className="text-muted small mb-3">Based on your usage patterns:</p>
            <ul className="list-group list-group-flush">
              {aiSuggestions.map((suggestion, index) => (
                <li key={index} className="list-group-item px-0">
                  <i className="fas fa-lightbulb text-warning me-2"></i>
                  {suggestion}
                </li>
              ))}
            </ul>
            <div className="text-center mt-3">
              <button
                className="btn btn-primary btn-sm"
                onClick={() => setShowAISuggestions(false)}
              >
                Apply Suggestions
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="footer">
        <div className="container-fluid">
          <div className="row">
            <div className="col-md-6">
              <p className="menu-text mb-2">TaskMaster - AI-Powered Task Management</p>
              <a href="/about/" className="footer-links">About</a>
              <a href="/contact/" className="footer-links">Contact</a>
              <a href="#" className="footer-links">Privacy Policy</a>
            </div>
            <div className="col-md-6 text-end">
              <p className="menu-text mb-2">© 2024 TaskMaster. All rights reserved.</p>
              <a href="#" className="footer-links">Terms of Service</a>
              <a href="#" className="footer-links">Support</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
