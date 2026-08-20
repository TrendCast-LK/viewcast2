import { Link } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

export default function Dashboard() {
  return (
    <div className="bg-background text-on-background min-h-screen font-body-md selection:bg-primary-fixed selection:text-on-primary-fixed">
      <Sidebar active="dashboard" />
      <Topbar />

      <main className="ml-64 pt-24 px-margin-desktop pb-24 max-w-container-max mx-auto flex flex-col gap-[64px]">
        <section className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="font-label-md text-label-md text-primary mb-2 uppercase tracking-widest">
              Dashboard Overview
            </p>
            <h2 className="font-display-lg text-display-lg text-on-background mb-4">
              Welcome back,{" "}
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Alex Chen
              </span>
            </h2>
            <div className="flex items-center gap-6 text-on-surface-variant">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined fill text-primary">group</span>
                <span className="font-headline-md text-headline-md">1.2M</span>
                <span className="font-body-md text-body-md text-tertiary">Subscribers</span>
              </div>
              <div className="w-px h-8 bg-outline-variant" />
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined fill text-secondary">visibility</span>
                <span className="font-headline-md text-headline-md">45.8M</span>
                <span className="font-body-md text-body-md text-tertiary">Monthly Views</span>
              </div>
            </div>
          </div>

          <Link
            to="/new-prediction"
            className="glass-panel p-8 rounded-[24px] shadow-[0_10px_30px_rgba(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgba(0,0,0,0.08)] hover:scale-[1.01] transition-all cursor-pointer group w-full md:w-[400px] relative overflow-hidden block"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-primary-fixed/40 to-secondary-fixed/40 z-0" />
            <div className="absolute -right-10 -top-10 w-32 h-32 bg-primary blur-3xl opacity-20 rounded-full" />
            <div className="relative z-10 flex flex-col items-start gap-4">
              <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center shadow-sm text-primary group-hover:scale-110 transition-transform">
                <span className="material-symbols-outlined">auto_awesome</span>
              </div>
              <div>
                <h3 className="font-headline-lg text-headline-lg text-on-background mb-2">
                  Analyze New Content
                </h3>
                <p className="font-body-md text-body-md text-on-surface-variant">
                  Upload a thumbnail or title to predict performance before publishing.
                </p>
              </div>
              <span className="mt-4 bg-primary text-white px-6 py-3 rounded-full font-label-md text-label-md flex items-center gap-2 group-hover:bg-on-primary-fixed-variant transition-colors">
                Start Prediction
                <span className="material-symbols-outlined text-sm">arrow_forward</span>
              </span>
            </div>
          </Link>
        </section>
      </main>
    </div>
  );
}
