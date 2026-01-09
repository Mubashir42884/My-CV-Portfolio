'use client';
import React, { useState } from 'react';
import Sidebar from '@/components/Sidebar';
import ScholarFeed from '@/components/ScholarFeed';
import Unpublished from '@/components/Unpublished';
import { Mail, GraduationCap } from 'lucide-react';

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);
  const [activeSection, setActiveSection] = useState('about');

  // Handle smooth scroll function
  const scrollToSection = (sectionId) => {
    setActiveSection(sectionId);
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <div className={`min-h-screen transition-colors duration-700 ${
      darkMode 
        ? 'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-slate-100' 
        : 'bg-gradient-to-br from-rose-50 via-pink-50 to-purple-50 text-slate-800'
    }`}>
      
      {/* Sidebar handles navigation and theme toggle */}
      <Sidebar 
        darkMode={darkMode} 
        setDarkMode={setDarkMode}
        activeSection={activeSection}
        scrollToSection={scrollToSection}
      />

      {/* Main Content Area */}
      <main className="ml-0 md:ml-80 p-8 md:p-12 transition-all duration-500">
        <div className="max-w-4xl mx-auto space-y-16">
          
          {/* ABOUT SECTION */}
          <section id="about" className="scroll-mt-8">
            <div className={`transition-all duration-700 rounded-2xl p-8 ${
              darkMode 
                ? 'bg-slate-800/50 backdrop-blur-sm border border-slate-700/50' 
                : 'bg-white/70 backdrop-blur-sm border border-purple-200/50'
            } shadow-xl`}>
              <h2 className={`text-3xl font-serif font-bold mb-6 flex items-center gap-3 ${
                darkMode ? 'text-slate-100' : 'text-slate-800'
              }`}>
                <GraduationCap className={darkMode ? 'text-indigo-400' : 'text-purple-500'} />
                About Me
              </h2>
              <div className={`font-serif leading-relaxed space-y-4 ${
                darkMode ? 'text-slate-300' : 'text-slate-700'
              }`}>
                <p>
                  Welcome to my academic portfolio. I am a Master of Computer Science student at 
                  Dalhousie University, currently navigating the intersection of Artificial Intelligence, 
                  Machine Learning, and Healthcare.
                </p>
                <p>
                  My research focuses on making AI interpretable and trustworthy, specifically in the 
                  context of data privacy and medical diagnostics. I specialize in Python, Data Analysis, 
                  and developing robust statistical models to solve real-world problems.
                </p>
              </div>
            </div>
          </section>

          {/* PUBLICATIONS SECTION */}
          <section id="publications" className="scroll-mt-8">
             <ScholarFeed darkMode={darkMode} />
          </section>

          {/* UNPUBLISHED WORKS SECTION */}
          <section id="unpublished" className="scroll-mt-8">
             <Unpublished darkMode={darkMode} />
          </section>

          {/* CONTACT SECTION */}
          <section id="contact" className="scroll-mt-8">
            <div className={`transition-all duration-700 rounded-2xl p-8 ${
              darkMode 
                ? 'bg-slate-800/50 backdrop-blur-sm border border-slate-700/50' 
                : 'bg-white/70 backdrop-blur-sm border border-purple-200/50'
            } shadow-xl`}>
              <h2 className={`text-3xl font-serif font-bold mb-6 flex items-center gap-3 ${
                darkMode ? 'text-slate-100' : 'text-slate-800'
              }`}>
                <Mail className={darkMode ? 'text-indigo-400' : 'text-purple-500'} />
                Get In Touch
              </h2>
              <div className={`font-serif leading-relaxed space-y-4 ${
                darkMode ? 'text-slate-300' : 'text-slate-700'
              }`}>
                <p>I'm always interested in collaboration opportunities and research discussions.</p>
                <div className="space-y-2 mt-6">
                  <p><strong>Email:</strong> mubashir.mohsin@dal.ca</p>
                  <p><strong>Institution:</strong> Dalhousie University</p>
                </div>
              </div>
            </div>
          </section>

        </div>
      </main>
    </div>
  );
}