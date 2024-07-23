import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://bmzebewzxpnheeuhuplh.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJtemViZXd6eHBuaGVldWh1cGxoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjExNzg0MzQsImV4cCI6MjAzNjc1NDQzNH0.sWY8GLXn2-8MMzNpYYShXejONE9qYWhRuW0IivQX2GM';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

