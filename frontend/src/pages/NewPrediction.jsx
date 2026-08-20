import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

export default function NewPrediction() {
  const navigate = useNavigate();

  function handleInitialize(e) {
    e.preventDefault();
    navigate("/prediction-result");
  }

  return (
    <div className="font-body-md text-body-md antialiased min-h-screen overflow-x-hidden bg-background text-on-background">
      <Sidebar active="predictions" />
      <Topbar searchPlaceholder="Search insights..." />

      <main className="ml-64 pt-24 px-margin-desktop pb-24 max-w-container-max mx-auto">
        <div className="mb-12">
          <h2 className="font-headline-lg text-headline-lg text-on-background mb-2">
            Create New Prediction
          </h2>
          <p className="font-body-lg text-body-lg text-on-surface-variant">
            Define the parameters for your next predictive model run.
          </p>
        </div>

        <form className="grid grid-cols-1 lg:grid-cols-12 gap-gutter" onSubmit={handleInitialize}>
          {/* Left column */}
          <div className="lg:col-span-7 flex flex-col gap-8">
            <div className="glass-panel p-8 rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgba(0,0,0,0.08)] transition-shadow duration-300">
              <h3 className="font-headline-md text-headline-md text-on-background mb-6 border-b border-outline-variant/50 pb-4">
                Basic Information
              </h3>
              <div className="space-y-6">
                <div>
                  <label className="block font-label-md text-label-md text-on-surface-variant mb-2">
                    Prediction Title
                  </label>
                  <input
                    className="input-field font-body-md text-body-md text-on-surface"
                    placeholder="e.g., Q4 Revenue Forecast"
                    type="text"
                  />
                </div>
                <div>
                  <label className="block font-label-md text-label-md text-on-surface-variant mb-2">
                    Category
                  </label>
                  <div className="relative">
                    <select className="input-field appearance-none font-body-md text-body-md text-on-surface cursor-pointer">
                      <option>Select a category</option>
                      <option>Financial Performance</option>
                      <option>User Engagement</option>
                      <option>Market Trends</option>
                    </select>
                    <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-on-surface-variant">
                      expand_more
                    </span>
                  </div>
                </div>
                <div>
                  <label className="block font-label-md text-label-md text-on-surface-variant mb-2">Tags</label>
                  <input
                    className="input-field font-body-md text-body-md text-on-surface mb-3"
                    placeholder="Add tags and press enter"
                    type="text"
                  />
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 bg-tertiary-fixed text-on-tertiary-fixed-variant rounded-full font-label-sm text-label-sm flex items-center gap-1 cursor-pointer hover:bg-tertiary-fixed-dim transition-colors">
                      Revenue <span className="material-symbols-outlined text-[14px]">close</span>
                    </span>
                    <span className="px-3 py-1 bg-tertiary-fixed text-on-tertiary-fixed-variant rounded-full font-label-sm text-label-sm flex items-center gap-1 cursor-pointer hover:bg-tertiary-fixed-dim transition-colors">
                      Q4 <span className="material-symbols-outlined text-[14px]">close</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="glass-panel p-8 rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgba(0,0,0,0.08)] transition-shadow duration-300">
              <h3 className="font-headline-md text-headline-md text-on-background mb-6 border-b border-outline-variant/50 pb-4">
                Schedule
              </h3>
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block font-label-md text-label-md text-on-surface-variant mb-2">
                    Target Date
                  </label>
                  <div className="relative">
                    <input className="input-field font-body-md text-body-md text-on-surface pl-10" type="date" />
                    <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none text-on-surface-variant">
                      calendar_today
                    </span>
                  </div>
                </div>
                <div>
                  <label className="block font-label-md text-label-md text-on-surface-variant mb-2">
                    Target Time (Optional)
                  </label>
                  <div className="relative">
                    <input className="input-field font-body-md text-body-md text-on-surface pl-10" type="time" />
                    <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none text-on-surface-variant">
                      schedule
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right column */}
          <div className="lg:col-span-5 flex flex-col gap-8">
            <div className="glass-panel p-8 rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.04)] flex-grow">
              <h3 className="font-headline-md text-headline-md text-on-background mb-6">Thumbnail &amp; Dataset</h3>
              <div className="border-2 border-dashed border-primary-fixed-dim bg-surface-container-lowest/50 rounded-xl p-8 flex flex-col items-center justify-center text-center cursor-pointer hover:bg-surface-container-lowest transition-colors h-64 mb-6 relative overflow-hidden group">
                <div className="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                <span className="material-symbols-outlined fill text-4xl text-primary mb-4">cloud_upload</span>
                <p className="font-body-md text-body-md text-on-surface font-medium mb-1">
                  Drag and drop file here
                </p>
                <p className="font-label-sm text-label-sm text-on-surface-variant">
                  or click to browse from device
                </p>
                <p className="font-label-sm text-label-sm text-outline mt-4">
                  Supports .csv, .json, .png, .jpg (Max 50MB)
                </p>
              </div>

              <div className="bg-surface-container rounded-xl p-6 mt-8">
                <div className="flex justify-between items-center mb-4">
                  <span className="font-label-md text-label-md text-on-surface">Initial Confidence Estimate</span>
                  <span className="material-symbols-outlined text-tertiary">info</span>
                </div>
                <div className="w-full bg-surface-container-highest rounded-full h-2 mb-2 overflow-hidden">
                  <div className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full w-[65%]" />
                </div>
                <p className="font-label-sm text-label-sm text-on-surface-variant text-right">
                  Pending full data upload...
                </p>
              </div>
            </div>

            <div className="flex gap-4 justify-end">
              <button
                className="px-6 py-3 bg-surface-container text-on-surface rounded-xl font-label-md text-label-md hover:bg-surface-container-highest transition-colors"
                type="button"
              >
                Save as Draft
              </button>
              <button
                className="px-6 py-3 bg-gradient-to-r from-primary to-secondary text-on-primary rounded-xl font-label-md text-label-md shadow-lg shadow-primary/20 hover:scale-[1.02] transition-transform active:scale-95 flex items-center gap-2"
                type="submit"
              >
                <span className="material-symbols-outlined text-[20px]">magic_button</span>
                Initialize Prediction
              </button>
            </div>
          </div>
        </form>
      </main>
    </div>
  );
}
