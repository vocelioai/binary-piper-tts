#!/usr/bin/env python3
"""
Binary Piper TTS - Performance Optimization Module
Advanced caching, memory management, and performance enhancements
"""

import os
import time
import json
import hashlib
import psutil
import threading
from datetime import datetime, timedelta
from collections import OrderedDict, defaultdict
from typing import Optional, Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceCache:
    """Advanced LRU cache with TTL and memory management"""
    
    def __init__(self, max_size=1000, ttl_seconds=3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache = OrderedDict()
        self.timestamps = {}
        self.hit_count = 0
        self.miss_count = 0
        self.lock = threading.RLock()
    
    def _is_expired(self, key):
        """Check if cache entry has expired"""
        if key not in self.timestamps:
            return True
        return time.time() - self.timestamps[key] > self.ttl_seconds
    
    def get(self, key):
        """Get value from cache"""
        with self.lock:
            if key in self.cache and not self._is_expired(key):
                # Move to end (most recently used)
                value = self.cache.pop(key)
                self.cache[key] = value
                self.hit_count += 1
                return value
            else:
                # Remove expired entry
                if key in self.cache:
                    del self.cache[key]
                    del self.timestamps[key]
                self.miss_count += 1
                return None
    
    def set(self, key, value):
        """Set value in cache"""
        with self.lock:
            # Remove oldest entries if at capacity
            while len(self.cache) >= self.max_size:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                del self.timestamps[oldest_key]
            
            self.cache[key] = value
            self.timestamps[key] = time.time()
    
    def clear_expired(self):
        """Remove all expired entries"""
        with self.lock:
            expired_keys = [k for k in self.cache.keys() if self._is_expired(k)]
            for key in expired_keys:
                del self.cache[key]
                del self.timestamps[key]
    
    def stats(self):
        """Get cache statistics"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate,
            "memory_usage_mb": self._estimate_memory_usage()
        }
    
    def _estimate_memory_usage(self):
        """Estimate memory usage of cache in MB"""
        try:
            import sys
            total_size = 0
            for key, value in self.cache.items():
                total_size += sys.getsizeof(key) + sys.getsizeof(value)
            return total_size / (1024 * 1024)  # Convert to MB
        except:
            return 0

class PerformanceMonitor:
    """Real-time performance monitoring"""
    
    def __init__(self):
        self.request_times = defaultdict(list)
        self.error_counts = defaultdict(int)
        self.voice_usage = defaultdict(int)
        self.text_length_stats = []
        self.start_time = time.time()
        self.lock = threading.Lock()
    
    def record_request(self, voice: str, text_length: int, response_time: float, success: bool):
        """Record a TTS request for analysis"""
        with self.lock:
            self.request_times[voice].append(response_time)
            self.voice_usage[voice] += 1
            self.text_length_stats.append(text_length)
            
            if not success:
                self.error_counts[voice] += 1
            
            # Keep only recent data (last 1000 requests per voice)
            if len(self.request_times[voice]) > 1000:
                self.request_times[voice] = self.request_times[voice][-1000:]
    
    def get_performance_stats(self):
        """Get comprehensive performance statistics"""
        with self.lock:
            uptime_hours = (time.time() - self.start_time) / 3600
            
            # Calculate overall stats
            all_times = []
            total_requests = 0
            total_errors = 0
            
            for voice, times in self.request_times.items():
                all_times.extend(times)
                total_requests += len(times)
                total_errors += self.error_counts.get(voice, 0)
            
            if not all_times:
                return {"error": "No performance data available"}
            
            # Voice performance analysis
            voice_stats = {}
            for voice, times in self.request_times.items():
                if times:
                    voice_stats[voice] = {
                        "avg_response_time": sum(times) / len(times),
                        "min_response_time": min(times),
                        "max_response_time": max(times),
                        "request_count": len(times),
                        "error_rate": (self.error_counts.get(voice, 0) / len(times)) * 100,
                        "usage_percentage": (len(times) / total_requests) * 100
                    }
            
            # Text length analysis
            text_stats = {}
            if self.text_length_stats:
                text_stats = {
                    "avg_length": sum(self.text_length_stats) / len(self.text_length_stats),
                    "min_length": min(self.text_length_stats),
                    "max_length": max(self.text_length_stats),
                    "total_characters": sum(self.text_length_stats)
                }
            
            return {
                "uptime_hours": uptime_hours,
                "total_requests": total_requests,
                "total_errors": total_errors,
                "error_rate": (total_errors / total_requests) * 100 if total_requests > 0 else 0,
                "avg_response_time": sum(all_times) / len(all_times),
                "min_response_time": min(all_times),
                "max_response_time": max(all_times),
                "voice_statistics": voice_stats,
                "text_statistics": text_stats,
                "top_voices": dict(sorted(self.voice_usage.items(), key=lambda x: x[1], reverse=True)[:10])
            }

class SystemResourceMonitor:
    """Monitor system resources (CPU, Memory, Disk)"""
    
    @staticmethod
    def get_resource_usage():
        """Get current system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count(),
                    "status": "high" if cpu_percent > 80 else "normal" if cpu_percent > 50 else "low"
                },
                "memory": {
                    "total_gb": memory.total / (1024**3),
                    "used_gb": memory.used / (1024**3),
                    "available_gb": memory.available / (1024**3),
                    "percent": memory.percent,
                    "status": "high" if memory.percent > 80 else "normal" if memory.percent > 50 else "low"
                },
                "disk": {
                    "total_gb": disk.total / (1024**3),
                    "used_gb": disk.used / (1024**3),
                    "free_gb": disk.free / (1024**3),
                    "percent": (disk.used / disk.total) * 100,
                    "status": "high" if (disk.used / disk.total) > 0.8 else "normal"
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to get resource usage: {e}"}

class OptimizedTTSProcessor:
    """Optimized TTS processing with caching and performance monitoring"""
    
    def __init__(self):
        self.audio_cache = PerformanceCache(max_size=500, ttl_seconds=1800)  # 30 min TTL
        self.text_cache = PerformanceCache(max_size=1000, ttl_seconds=3600)  # 1 hour TTL
        self.performance_monitor = PerformanceMonitor()
        self.resource_monitor = SystemResourceMonitor()
    
    def generate_cache_key(self, text: str, voice: str, **kwargs) -> str:
        """Generate a unique cache key for TTS request"""
        # Include all relevant parameters in cache key
        cache_data = {
            "text": text,
            "voice": voice,
            **kwargs
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get_cached_audio(self, text: str, voice: str, **kwargs):
        """Get cached audio if available"""
        cache_key = self.generate_cache_key(text, voice, **kwargs)
        return self.audio_cache.get(cache_key)
    
    def cache_audio(self, text: str, voice: str, audio_data: bytes, **kwargs):
        """Cache generated audio"""
        cache_key = self.generate_cache_key(text, voice, **kwargs)
        self.audio_cache.set(cache_key, audio_data)
    
    def record_performance(self, voice: str, text: str, response_time: float, success: bool):
        """Record performance metrics"""
        self.performance_monitor.record_request(
            voice=voice,
            text_length=len(text),
            response_time=response_time,
            success=success
        )
    
    def get_optimization_report(self):
        """Get comprehensive optimization report"""
        return {
            "audio_cache": self.audio_cache.stats(),
            "text_cache": self.text_cache.stats(),
            "performance": self.performance_monitor.get_performance_stats(),
            "resources": self.resource_monitor.get_resource_usage(),
            "recommendations": self.generate_recommendations()
        }
    
    def generate_recommendations(self):
        """Generate optimization recommendations"""
        recommendations = []
        
        # Cache analysis
        audio_stats = self.audio_cache.stats()
        if audio_stats["hit_rate"] < 30:
            recommendations.append({
                "type": "cache",
                "priority": "medium",
                "message": f"Audio cache hit rate is low ({audio_stats['hit_rate']:.1f}%). Consider increasing cache size or TTL."
            })
        
        # Resource analysis
        resources = self.resource_monitor.get_resource_usage()
        if not resources.get("error"):
            if resources["memory"]["status"] == "high":
                recommendations.append({
                    "type": "memory",
                    "priority": "high",
                    "message": f"Memory usage is high ({resources['memory']['percent']:.1f}%). Consider reducing cache sizes or restarting service."
                })
            
            if resources["cpu"]["status"] == "high":
                recommendations.append({
                    "type": "cpu",
                    "priority": "high", 
                    "message": f"CPU usage is high ({resources['cpu']['percent']:.1f}%). Consider load balancing or optimizing voice models."
                })
        
        # Performance analysis
        perf_stats = self.performance_monitor.get_performance_stats()
        if not perf_stats.get("error"):
            if perf_stats["avg_response_time"] > 3.0:
                recommendations.append({
                    "type": "performance",
                    "priority": "medium",
                    "message": f"Average response time is high ({perf_stats['avg_response_time']:.2f}s). Consider voice model optimization."
                })
        
        if not recommendations:
            recommendations.append({
                "type": "status",
                "priority": "info",
                "message": "System is performing well! No optimization recommendations at this time."
            })
        
        return recommendations
    
    def cleanup_caches(self):
        """Clean up expired cache entries"""
        self.audio_cache.clear_expired()
        self.text_cache.clear_expired()

def main():
    """Demo of performance optimization features"""
    print("⚡ BINARY PIPER TTS - PERFORMANCE OPTIMIZATION")
    print("=" * 60)
    
    processor = OptimizedTTSProcessor()
    
    # Simulate some usage
    print("📊 Generating optimization report...")
    report = processor.get_optimization_report()
    
    print(f"\n🎯 AUDIO CACHE PERFORMANCE:")
    audio_cache = report["audio_cache"]
    print(f"   Size: {audio_cache['size']}/{audio_cache['max_size']}")
    print(f"   Hit Rate: {audio_cache['hit_rate']:.1f}%")
    print(f"   Memory Usage: {audio_cache['memory_usage_mb']:.2f} MB")
    
    print(f"\n💾 SYSTEM RESOURCES:")
    resources = report["resources"]
    if not resources.get("error"):
        print(f"   CPU: {resources['cpu']['percent']:.1f}% ({resources['cpu']['status']})")
        print(f"   Memory: {resources['memory']['percent']:.1f}% ({resources['memory']['status']})")
        print(f"   Disk: {resources['disk']['percent']:.1f}% ({resources['disk']['status']})")
    else:
        print(f"   ❌ {resources['error']}")
    
    print(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
    for i, rec in enumerate(report["recommendations"], 1):
        priority_icon = "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "🟢"
        print(f"   {i}. {priority_icon} {rec['message']}")
    
    print("\n" + "=" * 60)
    print("✅ Performance optimization module ready!")

if __name__ == "__main__":
    main()
