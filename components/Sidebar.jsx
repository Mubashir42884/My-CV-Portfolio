import React from 'react';
import { Moon, Sun, ExternalLink, Mail, BookOpen, FileText, Award } from 'lucide-react';

const Sidebar = ({ darkMode, setDarkMode, activeSection, scrollToSection }) => {
  
  const navItems = [
    { id: 'about', label: 'About', icon: BookOpen },
    { id: 'publications', label: 'Publications', icon: FileText },
    { id: 'unpublished', label: 'Unpublished Works', icon: Award },
    { id: 'contact', label: 'Contact', icon: Mail }
  ];

  return (
    <aside className={`fixed left-0 top-0 h-full w-80 transition-all duration-700 ${
        darkMode 
          ? 'bg-slate-800/80 backdrop-blur-xl border-r border-slate-700/50' 
          : 'bg-white/80 backdrop-blur-xl border-r border-purple-200/50'
      } shadow-2xl z-50 hidden md:block`}>
        <div className="flex flex-col h-full p-8">
          
          {/* Profile Image */}
          <div className="flex justify-center mb-6">
            <div className={`relative w-36 h-36 rounded-full p-1 transition-all duration-500 ${
              darkMode 
                ? 'bg-gradient-to-br from-indigo-500 to-purple-600' 
                : 'bg-gradient-to-br from-rose-400 to-purple-400'
            } shadow-lg`}>
              {/* Ensure profile.jpg is in your public folder */}
              <img
                src="/profile.jpg" 
                alt="Mubashir Mohsin"
                className="w-full h-full rounded-full object-cover border-4 border-white/20"
              />
            </div>
          </div>

          {/* Name */}
          <div className="text-center mb-6">
            <h1 className={`text-2xl font-serif font-bold mb-2 transition-colors duration-500 ${
              darkMode ? 'text-slate-100' : 'text-slate-800'
            }`}>
              Mubashir Mohsin
            </h1>
            <p className={`text-sm font-serif transition-colors duration-500 ${
              darkMode ? 'text-slate-400' : 'text-slate-600'
            }`}>
              Master's Student • Research Enthusiast
            </p>
          </div>

          {/* Theme Toggle Button */}
          <div className="flex justify-center mb-6">
            <button
              onClick={() => setDarkMode(!darkMode)}
              className={`relative w-16 h-8 rounded-full transition-all duration-500 ${
                darkMode ? 'bg-indigo-900' : 'bg-amber-200'
              } shadow-inner`}
              aria-label="Toggle theme"
            >
              <div className={`absolute top-1 left-1 w-6 h-6 rounded-full transition-all duration-500 transform ${
                  darkMode ? 'translate-x-8 bg-slate-700' : 'translate-x-0 bg-amber-400'
                } flex items-center justify-center shadow-md`}>
                {darkMode ? <Moon className="w-4 h-4 text-indigo-200" /> : <Sun className="w-4 h-4 text-amber-700" />}
              </div>
            </button>
          </div>

          {/* Navigation Links */}
          <nav className="flex-1 space-y-2">
            {navItems.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => scrollToSection(id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 font-serif ${
                  activeSection === id
                    ? darkMode
                      ? 'bg-indigo-600/30 text-indigo-300 shadow-lg'
                      : 'bg-purple-200/50 text-purple-700 shadow-md'
                    : darkMode
                    ? 'text-slate-400 hover:bg-slate-700/50 hover:text-slate-200'
                    : 'text-slate-600 hover:bg-purple-100/50 hover:text-purple-700'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span>{label}</span>
              </button>
            ))}
          </nav>

          {/* External Links */}
          <div className="mt-6 pt-6 border-t border-slate-300/20">
            <div className="flex justify-center gap-4">
              {['Scholar', 'LinkedIn', 'GitHub'].map((platform) => (
                <a key={platform} href="#" className={`transition-all duration-300 ${
                    darkMode ? 'text-slate-400 hover:text-indigo-400' : 'text-slate-600 hover:text-purple-600'
                  } hover:scale-110`}>
                  <ExternalLink className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>
        </div>
      </aside>
  );
};
export default Sidebar;