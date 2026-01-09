import React, { useState, useEffect } from 'react';
import { FileText, Award } from 'lucide-react';

const ScholarFeed = ({ darkMode }) => {
  const [publications, setPublications] = useState([]);

  useEffect(() => {
    // Fetch from the local JSON file
    fetch('/scholar.json')
      .then((res) => res.json())
      .then((data) => setPublications(data))
      .catch((err) => console.error("Error loading scholar data:", err));
  }, []);

  return (
    <div className={`transition-all duration-700 rounded-2xl p-8 ${
      darkMode 
        ? 'bg-slate-800/50 backdrop-blur-sm border border-slate-700/50' 
        : 'bg-white/70 backdrop-blur-sm border border-purple-200/50'
    } shadow-xl`}>
      <h2 className={`text-3xl font-serif font-bold mb-6 flex items-center gap-3 ${
        darkMode ? 'text-slate-100' : 'text-slate-800'
      }`}>
        <FileText className={darkMode ? 'text-indigo-400' : 'text-purple-500'} />
        Publications
      </h2>
      <p className={`font-serif text-sm mb-6 ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>
        Auto-updated daily from Google Scholar
      </p>
      
      <div className="space-y-6">
        {publications.map((pub, index) => (
          <div key={index} className={`transition-all duration-500 p-6 rounded-xl ${
              darkMode 
                ? 'bg-slate-700/30 hover:bg-slate-700/50 border border-slate-600/30' 
                : 'bg-purple-50/50 hover:bg-purple-100/50 border border-purple-200/30'
            } hover:shadow-lg hover:scale-[1.01]`}>
            <h3 className={`font-serif font-semibold text-lg mb-2 ${
              darkMode ? 'text-slate-100' : 'text-slate-800'
            }`}>
              <a href={pub.url || pub.link} target="_blank" rel="noreferrer" className="hover:underline">
                {pub.title}
              </a>
            </h3>
            <p className={`font-serif text-sm mb-3 ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>
              {pub.authors}
            </p>
            <p className={`font-serif text-sm italic mb-3 ${darkMode ? 'text-slate-500' : 'text-slate-500'}`}>
              {pub.venue || pub.journal}
            </p>
            <div className="flex items-center gap-6 text-sm font-serif">
              <span className={`flex items-center gap-2 ${darkMode ? 'text-indigo-400' : 'text-purple-600'}`}>
                <Award className="w-4 h-4" />
                Cited by: {pub.citations}
              </span>
              <span className={darkMode ? 'text-slate-400' : 'text-slate-600'}>
                Year: {pub.year}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
export default ScholarFeed;