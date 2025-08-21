#!/usr/bin/env python3
"""
Binary Piper TTS - Enhanced Monitoring System
Real-time monitoring, alerting, and health checks
"""

import requests
import time
import json
import threading
from datetime import datetime, timezone, timedelta
from collections import deque, defaultdict
# Email imports removed for now - can be added later
# import smtplib
# from email.mime.text import MimeText
# from email.mime.multipart import MimeMultipart

class HealthMonitor:
    """Continuous health monitoring with alerting"""
    
    def __init__(self, base_url="https://binary-piper-tts-production.up.railway.app"):
        self.base_url = base_url
        self.is_monitoring = False
        self.health_history = deque(maxlen=1000)  # Keep last 1000 health checks
        self.alert_thresholds = {
            "response_time": 5.0,  # seconds
            "error_rate": 10.0,    # percentage
            "consecutive_failures": 3
        }
        self.consecutive_failures = 0
        self.last_alert_time = None
        self.alert_cooldown = 300  # 5 minutes between alerts
    
    def check_health(self):
        """Perform comprehensive health check"""
        start_time = time.time()
        health_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "response_time": None,
            "status": "unknown",
            "checks": {}
        }
        
        try:
            # Health endpoint check
            response = requests.get(f"{self.base_url}/health", timeout=10)
            health_data["response_time"] = time.time() - start_time
            health_data["status_code"] = response.status_code
            
            if response.status_code == 200:
                api_health = response.json()
                health_data["status"] = api_health.get("status", "unknown")
                health_data["checks"] = api_health.get("checks", {})
                health_data["healthy"] = True
                self.consecutive_failures = 0
            else:
                health_data["status"] = "unhealthy"
                health_data["error"] = f"HTTP {response.status_code}"
                health_data["healthy"] = False
                self.consecutive_failures += 1
                
        except Exception as e:
            health_data["response_time"] = time.time() - start_time
            health_data["status"] = "error"
            health_data["error"] = str(e)
            health_data["healthy"] = False
            self.consecutive_failures += 1
        
        # Additional checks
        health_data.update(self._additional_checks())
        
        # Store in history
        self.health_history.append(health_data)
        
        # Check for alerts
        self._check_alerts(health_data)
        
        return health_data
    
    def _additional_checks(self):
        """Perform additional health checks"""
        checks = {}
        
        try:
            # Voice endpoint check
            start_time = time.time()
            voices_response = requests.get(f"{self.base_url}/voices", timeout=10)
            voice_response_time = time.time() - start_time
            
            if voices_response.status_code == 200:
                voices = voices_response.json()
                checks["voices_endpoint"] = {
                    "status": "ok",
                    "response_time": voice_response_time,
                    "voice_count": len(voices) if isinstance(voices, list) else 0
                }
            else:
                checks["voices_endpoint"] = {
                    "status": "error",
                    "response_time": voice_response_time,
                    "error": f"HTTP {voices_response.status_code}"
                }
        except Exception as e:
            checks["voices_endpoint"] = {
                "status": "error",
                "error": str(e)
            }
        
        try:
            # Quick synthesis test
            start_time = time.time()
            test_response = requests.post(
                f"{self.base_url}/synthesize",
                json={"text": "test", "voice": "en_US-amy-low"},
                timeout=15
            )
            synthesis_time = time.time() - start_time
            
            if test_response.status_code == 200:
                checks["synthesis"] = {
                    "status": "ok",
                    "response_time": synthesis_time,
                    "audio_size": len(test_response.content)
                }
            else:
                checks["synthesis"] = {
                    "status": "error",
                    "response_time": synthesis_time,
                    "error": f"HTTP {test_response.status_code}"
                }
        except Exception as e:
            checks["synthesis"] = {
                "status": "error",
                "error": str(e)
            }
        
        return {"additional_checks": checks}
    
    def _check_alerts(self, health_data):
        """Check if any alerts should be triggered"""
        alerts = []
        
        # Response time alert
        if health_data.get("response_time", 0) > self.alert_thresholds["response_time"]:
            alerts.append(f"High response time: {health_data['response_time']:.2f}s")
        
        # Consecutive failures alert
        if self.consecutive_failures >= self.alert_thresholds["consecutive_failures"]:
            alerts.append(f"Service down: {self.consecutive_failures} consecutive failures")
        
        # Voice count alert (if significantly lower than expected)
        voice_check = health_data.get("additional_checks", {}).get("voices_endpoint", {})
        voice_count = voice_check.get("voice_count", 0)
        if voice_count < 30:  # Assuming we expect at least 30 voices
            alerts.append(f"Low voice count: only {voice_count} voices available")
        
        if alerts:
            self._send_alerts(alerts, health_data)
    
    def _send_alerts(self, alerts, health_data):
        """Send alerts (console for now, can be extended to email/webhook)"""
        current_time = time.time()
        
        # Check cooldown
        if (self.last_alert_time and 
            current_time - self.last_alert_time < self.alert_cooldown):
            return
        
        print(f"\n🚨 ALERT - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("=" * 60)
        for alert in alerts:
            print(f"   ⚠️  {alert}")
        print(f"   📊 Current status: {health_data.get('status', 'unknown')}")
        print("=" * 60)
        
        self.last_alert_time = current_time
    
    def start_monitoring(self, interval=60):
        """Start continuous monitoring"""
        if self.is_monitoring:
            print("⚠️  Monitoring is already running")
            return
        
        self.is_monitoring = True
        print(f"🎯 Starting health monitoring (interval: {interval}s)")
        
        def monitor_loop():
            while self.is_monitoring:
                try:
                    health = self.check_health()
                    status_icon = "✅" if health.get("healthy") else "❌"
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    response_time = health.get("response_time", 0)
                    
                    print(f"{status_icon} [{timestamp}] Health: {health.get('status', 'unknown')} "
                          f"({response_time:.2f}s)")
                    
                except Exception as e:
                    print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Monitor error: {e}")
                
                time.sleep(interval)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        if not self.is_monitoring:
            print("⚠️  Monitoring is not running")
            return
        
        self.is_monitoring = False
        print("🛑 Stopping health monitoring")
    
    def get_health_summary(self, hours=24):
        """Get health summary for the last N hours"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        recent_checks = [
            check for check in self.health_history
            if datetime.fromisoformat(check["timestamp"].replace("Z", "+00:00")) > cutoff_time
        ]
        
        if not recent_checks:
            return {"error": "No health data available"}
        
        total_checks = len(recent_checks)
        healthy_checks = sum(1 for check in recent_checks if check.get("healthy", False))
        avg_response_time = sum(check.get("response_time", 0) for check in recent_checks) / total_checks
        
        return {
            "period_hours": hours,
            "total_checks": total_checks,
            "healthy_checks": healthy_checks,
            "uptime_percentage": (healthy_checks / total_checks) * 100,
            "avg_response_time": avg_response_time,
            "max_response_time": max((check.get("response_time", 0) for check in recent_checks), default=0),
            "recent_status": recent_checks[-1].get("status", "unknown") if recent_checks else "unknown"
        }

class MetricsCollector:
    """Collect and aggregate metrics over time"""
    
    def __init__(self):
        self.metrics = defaultdict(deque)
        self.max_history = 10000  # Keep last 10k data points
        
    def record_metric(self, name: str, value: float, timestamp=None):
        """Record a metric value"""
        if timestamp is None:
            timestamp = time.time()
        
        metric_data = {"value": value, "timestamp": timestamp}
        
        self.metrics[name].append(metric_data)
        
        # Keep only recent data
        if len(self.metrics[name]) > self.max_history:
            self.metrics[name].popleft()
    
    def get_metric_summary(self, name: str, hours=1):
        """Get summary statistics for a metric"""
        if name not in self.metrics:
            return {"error": f"Metric '{name}' not found"}
        
        cutoff_time = time.time() - (hours * 3600)
        recent_data = [
            point for point in self.metrics[name]
            if point["timestamp"] > cutoff_time
        ]
        
        if not recent_data:
            return {"error": "No recent data available"}
        
        values = [point["value"] for point in recent_data]
        
        return {
            "metric": name,
            "period_hours": hours,
            "count": len(values),
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "latest": values[-1] if values else None
        }

def main():
    """Demo of enhanced monitoring system"""
    print("🎯 BINARY PIPER TTS - ENHANCED MONITORING SYSTEM")
    print("=" * 70)
    
    # Initialize monitoring
    monitor = HealthMonitor()
    
    print("🔍 Running initial health check...")
    health = monitor.check_health()
    
    status_icon = "✅" if health.get("healthy") else "❌"
    print(f"{status_icon} Status: {health.get('status', 'unknown')}")
    print(f"⚡ Response Time: {health.get('response_time', 0):.2f}s")
    
    if "additional_checks" in health:
        print("\n📊 Additional Checks:")
        for check_name, check_data in health["additional_checks"].items():
            check_status = "✅" if check_data.get("status") == "ok" else "❌"
            print(f"   {check_status} {check_name}: {check_data.get('status', 'unknown')}")
    
    print(f"\n📈 Health Summary (Last 24h):")
    summary = monitor.get_health_summary()
    if "error" not in summary:
        print(f"   Uptime: {summary['uptime_percentage']:.1f}%")
        print(f"   Avg Response: {summary['avg_response_time']:.2f}s")
        print(f"   Total Checks: {summary['total_checks']}")
    else:
        print(f"   {summary['error']}")
    
    print(f"\n💡 Monitoring Features:")
    print("   🔄 Continuous health monitoring")
    print("   🚨 Automatic alerting system")
    print("   📊 Performance metrics collection")
    print("   📈 Historical data analysis")
    print("   ⚡ Real-time status updates")
    
    print("\n" + "=" * 70)
    print("✅ Enhanced monitoring system ready!")
    print("💡 Use monitor.start_monitoring(60) to begin continuous monitoring")

if __name__ == "__main__":
    main()
