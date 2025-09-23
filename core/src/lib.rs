pub fn encode(input: &[u8]) -> Vec<u8> {
    // Map elke byte v -> u16 f = 400 + 50*v (LE)
    let mut out = Vec::with_capacity(input.len() * 2);
    for &v in input {
        let f: u16 = 400 + 50 * (v as u16);
        out.extend_from_slice(&f.to_le_bytes());
    }
    out
}

pub fn decode(input: &[u8]) -> Result<Vec<u8>, String> {
    if input.len() % 2 != 0 {
        return Err("Invalid length for frequency stream".into());
    }
    let mut out = Vec::with_capacity(input.len() / 2);
    for chunk in input.chunks_exact(2) {
        let f = u16::from_le_bytes([chunk[0], chunk[1]]);
        if f < 400 { return Err("Frequency below base".into()); }
        let d = f - 400;
        if d % 50 != 0 { return Err("Frequency not aligned to 50 Hz steps".into()); }
        let v = (d / 50) as u8;
        out.push(v);
    }
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn roundtrip() {
        let data = b"hello PAXECT";
        let enc = encode(data);
        let dec = decode(&enc).unwrap();
        assert_eq!(dec, data);
    }
}
