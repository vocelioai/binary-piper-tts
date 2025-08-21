#!/usr/bin/env python3
"""
Binary Piper TTS - Integrated Production Dashboard
Complete production optimization, monitoring, and analytics
"""

import time
import json
import threading
from datetime import datetime, timezone
from production_analytics import ProductionAnalytics
from performance_optimization import OptimizedTTSProcessor
from enhanced_monitoring import HealthMonitor, MetricsCollector

class ProductionDashboard:
    """Integrated production dashboard with all optimization features"""
    
    def __init__(self, base_url="https://binary-piper-tts-production.up.railway.app"):
        self.base_url = base_url
        self.analytics = ProductionAnalytics(base_url)
        self.processor = OptimizedTTSProcessor()
        self.monitor = HealthMonitor(base_url)
        self.metrics = MetricsCollector()
        self.dashboard_active = False
        
    def start_dashboard(self):
        """Start the integrated production dashboard"""
        print("🚀 STARTING BINARY PIPER TTS PRODUCTION DASHBOARD")
        print("=" * 80)
        
        # Initial system check
        print("🔍 Running initial system analysis...")
        self._run_initial_analysis()
        
        # Start continuous monitoring
        print("\n🎯 Starting continuous monitoring...")
        self.monitor.start_monitoring(interval=120)  # 2-minute intervals
        
        # Start dashboard loop
        self.dashboard_active = True
        self._start_dashboard_loop()
        
    def _run_initial_analysis(self):
        """Run comprehensive initial analysis"""
        print("\n📊 INITIAL SYSTEM ANALYSIS")
        print("-" * 50)
        
        # Get system health
        health = self.monitor.check_health()
        status_icon = "✅" if health.get("healthy") else "❌"
        print(f"{status_icon} System Status: {health.get('status', 'unknown')}")
        print(f"⚡ Response Time: {health.get('response_time', 0):.2f}s")
        
        # Voice analytics
        voice_analytics = self.analytics.get_voices_analytics()
        if "error" not in voice_analytics:
            print(f"🎵 Total Voices: {voice_analytics['total_voices']}")
            print(f"🌍 Languages: {voice_analytics['language_diversity']}")
            print(f"🗺️  Regions: {voice_analytics['region_diversity']}")
            
            print("\n🏆 Top 3 Languages:")
            for lang, count in list(voice_analytics['top_languages'].items())[:3]:
                print(f"   {lang.upper()}: {count} voices")
        
        # Performance optimization report
        opt_report = self.processor.get_optimization_report()
        print(f"\n⚡ PERFORMANCE STATUS")
        print(f"   Cache Hit Rate: {opt_report['audio_cache']['hit_rate']:.1f}%")
        print(f"   Memory Usage: {opt_report['resources']['memory']['percent']:.1f}%")
        print(f"   CPU Usage: {opt_report['resources']['cpu']['percent']:.1f}%")
        
        # Recommendations
        print(f"\n💡 KEY RECOMMENDATIONS:")
        for i, rec in enumerate(opt_report['recommendations'][:3], 1):
            priority_icon = "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "🟢"
            print(f"   {i}. {priority_icon} {rec['message']}")
    
    def _start_dashboard_loop(self):
        """Start the main dashboard monitoring loop"""
        def dashboard_loop():
            loop_count = 0
            
            while self.dashboard_active:
                try:
                    loop_count += 1
                    current_time = datetime.now().strftime("%H:%M:%S")
                    
                    # Every 10 minutes, show detailed status
                    if loop_count % 5 == 0:  # 10 minutes (5 * 2-minute intervals)
                        print(f"\n📊 [{current_time}] DASHBOARD STATUS UPDATE")
                        print("-" * 50)
                        
                        # Quick health check
                        health = self.monitor.check_health()
                        status_icon = "✅" if health.get("healthy") else "❌"
                        print(f"{status_icon} Health: {health.get('status', 'unknown')} "
                              f"({health.get('response_time', 0):.2f}s)")
                        
                        # Health summary
                        summary = self.monitor.get_health_summary(hours=1)
                        if "error" not in summary:
                            print(f"📈 Last Hour: {summary['uptime_percentage']:.1f}% uptime, "
                                  f"{summary['avg_response_time']:.2f}s avg response")
                        
                        # Resource status
                        resources = self.processor.resource_monitor.get_resource_usage()
                        if "error" not in resources:
                            cpu_status = resources['cpu']['status']
                            mem_status = resources['memory']['status']
                            cpu_icon = "🟢" if cpu_status == "low" else "🟡" if cpu_status == "normal" else "🔴"
                            mem_icon = "🟢" if mem_status == "low" else "🟡" if mem_status == "normal" else "🔴"
                            print(f"💾 Resources: {cpu_icon} CPU {resources['cpu']['percent']:.1f}% "
                                  f"{mem_icon} Memory {resources['memory']['percent']:.1f}%")
                        
                        # Cache performance
                        cache_stats = self.processor.audio_cache.stats()
                        cache_icon = "🟢" if cache_stats['hit_rate'] > 50 else "🟡" if cache_stats['hit_rate'] > 20 else "🔴"
                        print(f"⚡ Cache: {cache_icon} {cache_stats['hit_rate']:.1f}% hit rate, "
                              f"{cache_stats['size']}/{cache_stats['max_size']} entries")
                        
                        # Clean up caches
                        self.processor.cleanup_caches()
                    
                    time.sleep(120)  # 2 minutes
                    
                except Exception as e:
                    print(f"❌ Dashboard error: {e}")
                    time.sleep(120)
        
        self.dashboard_thread = threading.Thread(target=dashboard_loop, daemon=True)
        self.dashboard_thread.start()
        print("✅ Dashboard monitoring loop started!")
    
    def stop_dashboard(self):
        """Stop the production dashboard"""
        print("\n🛑 STOPPING PRODUCTION DASHBOARD")
        self.dashboard_active = False
        self.monitor.stop_monitoring()
        print("✅ Dashboard stopped successfully!")
    
    def get_full_report(self):
        """Generate comprehensive production report"""
        print("📋 GENERATING COMPREHENSIVE PRODUCTION REPORT")
        print("=" * 80)
        
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system_health": self.monitor.check_health(),
            "voice_analytics": self.analytics.get_voices_analytics(),
            "performance_metrics": self.analytics.performance_benchmark(),
            "optimization_status": self.processor.get_optimization_report(),
            "health_summary": self.monitor.get_health_summary(hours=24)
        }
        
        # Save report to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"production_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📁 Full production report saved: {filename}")
        return report
    
    def run_interactive_mode(self):
        """Run dashboard in interactive mode"""
        print("🎮 INTERACTIVE PRODUCTION DASHBOARD")
        print("=" * 60)
        print("Commands:")
        print("  'status' - Show current status")
        print("  'health' - Run health check")
        print("  'perf' - Run performance benchmark")
        print("  'report' - Generate full report")
        print("  'start' - Start continuous monitoring")
        print("  'stop' - Stop monitoring")
        print("  'quit' - Exit dashboard")
        print("-" * 60)
        
        while True:
            try:
                command = input("\nDashboard> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    if self.dashboard_active:
                        self.stop_dashboard()
                    print("👋 Goodbye!")
                    break
                
                elif command == 'status':
                    self._show_quick_status()
                
                elif command == 'health':
                    health = self.monitor.check_health()
                    status_icon = "✅" if health.get("healthy") else "❌"
                    print(f"{status_icon} Health: {health.get('status')} "
                          f"({health.get('response_time', 0):.2f}s)")
                
                elif command == 'perf':
                    print("🔥 Running performance benchmark...")
                    perf = self.analytics.performance_benchmark(sample_voices=3)
                    if "error" not in perf:
                        metrics = perf.get("performance_metrics", {})
                        print(f"⚡ Average: {metrics.get('avg_response_time', 0):.2f}s")
                        print(f"✅ Success Rate: {metrics.get('success_rate', 0):.1f}%")
                
                elif command == 'report':
                    self.get_full_report()
                
                elif command == 'start':
                    if not self.dashboard_active:
                        self.start_dashboard()
                    else:
                        print("⚠️  Dashboard is already running")
                
                elif command == 'stop':
                    if self.dashboard_active:
                        self.stop_dashboard()
                    else:
                        print("⚠️  Dashboard is not running")
                
                elif command == 'help':
                    print("Available commands: status, health, perf, report, start, stop, quit")
                
                else:
                    print("❓ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Dashboard interrupted")
                if self.dashboard_active:
                    self.stop_dashboard()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_quick_status(self):
        """Show quick system status"""
        print("📊 QUICK STATUS")
        print("-" * 30)
        
        # Health
        health = self.monitor.check_health()
        status_icon = "✅" if health.get("healthy") else "❌"
        print(f"{status_icon} {health.get('status', 'unknown')} ({health.get('response_time', 0):.2f}s)")
        
        # Voices
        voice_analytics = self.analytics.get_voices_analytics()
        if "error" not in voice_analytics:
            print(f"🎵 {voice_analytics['total_voices']} voices ({voice_analytics['language_diversity']} languages)")
        
        # Resources
        resources = self.processor.resource_monitor.get_resource_usage()
        if "error" not in resources:
            print(f"💾 CPU: {resources['cpu']['percent']:.1f}% Memory: {resources['memory']['percent']:.1f}%")
        
        # Monitoring status
        monitoring_status = "🟢 Running" if self.dashboard_active else "🔴 Stopped"
        print(f"🎯 Monitoring: {monitoring_status}")

def main():
    """Main dashboard entry point"""
    dashboard = ProductionDashboard()
    
    print("🎯 BINARY PIPER TTS - PRODUCTION DASHBOARD")
    print("=" * 80)
    print("Choose an option:")
    print("  1. Quick Status Check")
    print("  2. Start Continuous Monitoring")
    print("  3. Generate Full Report")
    print("  4. Interactive Mode")
    print("  5. Exit")
    
    try:
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            dashboard._show_quick_status()
        
        elif choice == '2':
            dashboard.start_dashboard()
            print("\n💡 Dashboard is running! Press Ctrl+C to stop.")
            try:
                while dashboard.dashboard_active:
                    time.sleep(1)
            except KeyboardInterrupt:
                dashboard.stop_dashboard()
        
        elif choice == '3':
            dashboard.get_full_report()
        
        elif choice == '4':
            dashboard.run_interactive_mode()
        
        elif choice == '5':
            print("👋 Goodbye!")
        
        else:
            print("❓ Invalid option selected")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard interrupted")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")

if __name__ == "__main__":
    main()
