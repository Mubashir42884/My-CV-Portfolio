import React, { useState, useEffect } from 'react';
import { Award } from 'lucide-react';
import Papa from 'papaparse';

const Unpublished = ({ darkMode }) => {
  const [works, setWorks] = useState([]);

  useEffect(() => {
    // Parse the CSV file from public folder
    Papa.parse('/unpublished.csv', {
      download: true,
      header: true,
      complete: (results) => {
        // Filter out empty rows
        setWorks(results.data.filter(w => w.Title));
      },
      error: (err) => console.error("Error loading CSV:", err)
    });
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
        <Award className={darkMode ? 'text-indigo-400' : 'text-purple-500'} />
        Unpublished Works
      </h2>
      <p className={`font-serif text-sm mb-6 ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>
        Works in progress and under review
      </p>
      
      <div className="space-y-4">
        {works.map((work, index) => (
          <div key={index} className={`transition-all duration-500 p-5 rounded-xl ${
              darkMode 
                ? 'bg-slate-700/30 border border-slate-600/30 hover:bg-slate-700/50' 
                : 'bg-rose-50/50 border border-rose-200/30 hover:bg-rose-100/50'
            } hover:shadow-md`}>
            <p className={`font-serif ${darkMode ? 'text-slate-200' : 'text-slate-700'}`}>
              <span className="font-semibold">{work.Title}</span>. {work.Contributors} ({work.Year}).
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
export default Unpublished;