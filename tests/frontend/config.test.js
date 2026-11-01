import { describe, it, expect } from 'vitest';
import { CONFIG, API_BASE, ENVIRONMENT } from '../../src/config.js';

describe('Frontend Configuration', () => {
  it('should have configuration defined for development and production', () => {
    expect(CONFIG).toBeDefined();
    expect(CONFIG.development).toBeDefined();
    expect(CONFIG.production).toBeDefined();
    expect(CONFIG.development.API_BASE).toContain('http');
  });

  it('should have a valid environment and API_BASE', () => {
    expect(['development', 'production', 'staging']).toContain(ENVIRONMENT);
    expect(typeof API_BASE).toBe('string');
    expect(API_BASE.length).toBeGreaterThan(0);
  });
});

