<template>
  <div class="landing-page">
    <section class="hero-v3 relative overflow-hidden">
      <!-- Added a localized glowing stage light effect -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-4xl bg-[radial-gradient(ellipse_at_top,_var(--brand-glow),_transparent_70%)] opacity-30 mix-blend-screen pointer-events-none"></div>

      <div class="container text-center animate-corp relative z-10">
        <span class="badge-corp backdrop-blur-md bg-black/40 border-[var(--brand-primary)]/30 text-[var(--brand-primary)]">The Ultimate Gig Platform</span>
        <h1 class="hero-main-title delay-100 text-5xl md:text-7xl font-900 tracking-tighter mt-6">
          Book The Best <br/> <span class="text-gradient">Live Shows.</span>
        </h1>
        <p class="hero-description delay-200 text-lg text-white/70 max-w-2xl mx-auto mt-6 mb-10">
          The easiest way to organize, discover, and drop into the biggest parties and live events. Scale your gigs, manage guest lists, and ignite the dance floor.
        </p>
        <div class="hero-actions delay-300 flex justify-center gap-4">
          <router-link to="/register" class="btn-corp bg-[var(--brand-primary)] text-black hover:bg-white hover:shadow-[0_0_30px_var(--brand-glow)] hover:-translate-y-1 transition-all duration-300 font-900 px-8 py-4 text-sm">
            Join The Party
          </router-link>
          <router-link to="/login" class="btn-corp btn-corp-outline border-white/20 hover:border-white hover:bg-white/10 px-8 py-4 text-sm font-800 backdrop-blur-sm">
            Guest List
          </router-link>
        </div>
      </div>
    </section>

    <section class="section-spacer relative">
      <div class="container relative z-10">
        <div class="section-header text-center animate-corp">
          <h2 class="section-title-large text-4xl font-900 tracking-tight">The VIP Experience</h2>
          <p class="section-subtitle mt-2 text-[var(--text-muted)] uppercase tracking-widest text-sm font-800">Everything you need to run a massive night</p>
        </div>

        <div class="capabilities-grid mt-20">
          <div class="card-premium cap-card animate-corp delay-100 hover:border-[var(--brand-primary)]/50 transition-all shadow-luxury relative overflow-hidden group">
            <div class="absolute inset-0 bg-gradient-to-br from-[var(--brand-primary)]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="cap-icon-box relative z-10 flex border border-[var(--brand-primary)]/30 bg-[var(--brand-primary)]/5 rounded-2xl w-14 h-14 items-center justify-center mb-6">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--brand-primary)" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
            </div>
            <h3 class="relative z-10 text-white font-900 text-xl tracking-tight mb-3">Gig Management</h3>
            <p class="relative z-10 text-white/60 leading-relaxed font-500">Easily manage your lineups, venues, and set times from a single unified dashboard.</p>
          </div>
          
          <div class="card-premium cap-card animate-corp delay-200 hover:border-[var(--brand-secondary)]/50 transition-all shadow-luxury relative overflow-hidden group">
            <div class="absolute inset-0 bg-gradient-to-br from-[var(--brand-secondary)]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
             <div class="cap-icon-box relative z-10 flex border border-[var(--brand-secondary)]/30 bg-[var(--brand-secondary)]/5 rounded-2xl w-14 h-14 items-center justify-center mb-6">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--brand-secondary)" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
            </div>
            <h3 class="relative z-10 text-white font-900 text-xl tracking-tight mb-3">Hype Analytics</h3>
            <p class="relative z-10 text-white/60 leading-relaxed font-500">Track your ticket sales, drops, and audience engagement with live data streams.</p>
          </div>

          <div class="card-premium cap-card animate-corp delay-300 hover:border-[var(--brand-accent)]/50 transition-all shadow-luxury relative overflow-hidden group">
            <div class="absolute inset-0 bg-gradient-to-br from-[var(--brand-accent)]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="cap-icon-box relative z-10 flex border border-[var(--brand-accent)]/30 bg-[var(--brand-accent)]/5 rounded-2xl w-14 h-14 items-center justify-center mb-6">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--brand-accent)" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
            </div>
            <h3 class="relative z-10 text-white font-900 text-xl tracking-tight mb-3">Secure Entry</h3>
            <p class="relative z-10 text-white/60 leading-relaxed font-500">Automated access control so you can keep the lines moving and the fake tickets out.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section-spacer">
      <div class="container">
        <div class="portal-grid">
          <div class="card-premium portal-card-v2 animate-corp hover:border-[#00f3ff]/50 transition-all shadow-luxury relative overflow-hidden group">
            <div class="absolute inset-0 bg-gradient-to-br from-[#00f3ff]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="portal-header relative z-10 flex items-center justify-between mb-4">
              <span class="badge-corp bg-[#00f3ff]/10 text-[#00f3ff] border-[#00f3ff]/20">Party Goers</span>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--brand-secondary)" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            </div>
            <h3 class="text-white font-900 text-2xl mb-2 relative z-10">Get on the List</h3>
            <p class="relative z-10 text-white/60 flex-grow leading-relaxed">Find massive events, secure your tickets instantly, and never miss a beat.</p>
            <router-link to="/login" class="btn-corp bg-[#00f3ff] text-black w-full mt-8 relative z-10 hover:bg-white hover:shadow-[0_0_20px_rgba(0,243,255,0.4)] px-4 py-3 font-900 text-sm flex justify-between items-center transition-all duration-300">
              <span>Grab Tickets</span>
              <span>&rarr;</span>
            </router-link>
          </div>
          
          <div class="card-premium portal-card-v2 animate-corp delay-100 hover:border-[#ff007f]/50 transition-all shadow-luxury relative overflow-hidden group">
             <div class="absolute inset-0 bg-gradient-to-br from-[#ff007f]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="portal-header relative z-10 flex items-center justify-between mb-4">
              <span class="badge-corp bg-[#ff007f]/10 text-[#ff007f] border-[#ff007f]/20">Gig Vendors</span>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--brand-primary)" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            </div>
            <h3 class="text-white font-900 text-2xl mb-2 relative z-10">Host the Show</h3>
            <p class="relative z-10 text-white/60 flex-grow leading-relaxed">Drop your event details, manage your ticket sales, and pack the venue.</p>
            <router-link to="/login" class="btn-corp btn-corp-outline w-full mt-8 relative z-10 border-[#ff007f] text-[#ff007f] hover:bg-[#ff007f] hover:text-black hover:shadow-[0_0_20px_rgba(255,0,127,0.4)] px-4 py-3 font-900 text-sm flex justify-between items-center transition-all duration-300 backdrop-blur-sm">
              <span>Vendor Dashboard</span>
              <span>&rarr;</span>
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.landing-page {
  background: transparent;
}

.hero-main-title {
  margin: 1rem 0 1.5rem;
}

.capabilities-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.cap-card {
  padding: 2rem;
}

.cap-card h3 {
  margin: 1.25rem 0 0.75rem;
  font-size: 1.1rem;
  letter-spacing: -0.02em;
}

.cap-card p {
  color: var(--text-dim);
  font-size: 0.9rem;
  line-height: 1.5;
}

.cap-icon-box {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
}

.portal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.portal-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.portal-card-v2 {
  padding: 2rem;
}

.portal-card-v2 h3 {
  font-size: 1.25rem;
  margin: 0;
  line-height: 1.2;
}

.portal-card-v2 p {
  color: var(--text-dim);
  font-size: 0.9rem;
  line-height: 1.5;
}

.mt-20 { margin-top: 3rem; }

@media (max-width: 1024px) {
  .capabilities-grid, .portal-grid {
    grid-template-columns: 1fr;
  }
}
</style>
