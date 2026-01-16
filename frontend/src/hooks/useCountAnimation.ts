import { useEffect, useState } from 'react';

interface UseCountAnimationProps {
  end: number;
  duration?: number; // in milliseconds
  start?: number;
  delay?: number; // delay before starting animation
}

export const useCountAnimation = ({ 
  end, 
  duration = 2000, 
  start = 0,
  delay = 0
}: UseCountAnimationProps) => {
  const [count, setCount] = useState(start);

  useEffect(() => {
    let startTime: number;
    let animationFrame: number;
    let timeoutId: number;

    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime;
      const progress = Math.min((currentTime - startTime) / duration, 1);

      // Easing function for smooth animation (easeOutExpo)
      const easedProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      
      setCount(Math.floor(easedProgress * (end - start) + start));

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    // Start animation after delay
    if (delay > 0) {
      timeoutId = window.setTimeout(() => {
        animationFrame = requestAnimationFrame(animate);
      }, delay);
    } else {
      animationFrame = requestAnimationFrame(animate);
    }

    return () => {
      cancelAnimationFrame(animationFrame);
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [end, duration, start, delay]);

  return count;
};

