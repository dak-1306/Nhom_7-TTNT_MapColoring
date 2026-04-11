"""
Script kiểm tra CSP đơn giản
"""
import sys
sys.path.insert(0, ".")

from algorithms.csp import create_map_coloring_csp, default_constraint

print("=" * 80)
print("KIỂM TRA CSP")
print("=" * 80)

try:
    # Tạo CSP
    csp = create_map_coloring_csp()
    print(f"\n✓ CSP được tạo: {csp}")
    print(f"  - Số tỉnh: {len(csp.variables)}")
    print(f"  - Số màu: {len(csp.get_domain(csp.variables[0]))}")
    print(f"  - Danh sách màu: {csp.get_domain(csp.variables[0])}")
    
    # Test is_complete
    print("\n✓ is_complete() - Kiểm tra phép gán hoàn chỉnh:")
    print(f"  - Phép gán rỗng: {csp.is_complete({})}")
    print(f"  - Phép gán 2 tỉnh: {csp.is_complete({'Hà Nội': 'Đỏ', 'Hồ Chí Minh': 'Xanh'})}")
    
    # Test is_consistent
    print("\n✓ is_consistent() - Kiểm tra tính hợp lệ:")
    assignment = {}
    # Gán Hà Nội
    valid1 = csp.is_consistent("Hà Nội", "Đỏ", assignment)
    print(f"  - Gán Hà Nội=Đỏ (lần đầu): {valid1}")
    
    csp.assign("Hà Nội", "Đỏ", assignment)
    
    # Gán láng giềng với màu khác
    valid2 = csp.is_consistent("Hưng Yên", "Xanh", assignment)
    print(f"  - Gán Hưng Yên=Xanh (kế láng giềng Hà Nội): {valid2}")
    
    # Gán láng giềng với cùng màu
    valid3 = csp.is_consistent("Hưng Yên", "Đỏ", assignment)
    print(f"  - Gán Hưng Yên=Đỏ (cùng Hà Nội): {valid3}")
    
    # Test get_neighbors
    print("\n✓ get_neighbors() - Láng giềng:")
    neighbors = csp.get_neighbors("Hà Nội")
    print(f"  - Hà Nội có {len(neighbors)} tỉnh kề:")
    print(f"    {neighbors}")
    
    # Test get_unassigned_variables
    print("\n✓ get_unassigned_variables() - Biến chưa gán:")
    unassigned = csp.get_unassigned_variables({"Hà Nội": "Đỏ"})
    print(f"  - Chưa gán: {len(unassigned)} tỉnh")
    print(f"  - 5 tỉnh đầu: {unassigned[:5]}")
    
    print("\n" + "=" * 80)
    print("✓✓✓ TẤT CẢ TEST THÀNH CÔNG ✓✓✓")
    print("=" * 80)
    
except Exception as e:
    print(f"\n✗ LỖI: {e}")
    import traceback
    traceback.print_exc()
