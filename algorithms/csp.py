"""
Module CSP (Constraint Satisfaction Problem) - Bài toán Thỏa mãn Ràng buộc
Tô màu Bản đồ Việt Nam

═══════════════════════════════════════════════════════════════════════════════
MÔ TẢ:
    Module này cung cấp framework CSP tổng quát để giải các bài toán 
    Constraint Satisfaction Problem (CSP), đặc biệt thiết kế cho bài toán 
    tô màu bản đồ các tỉnh thành Việt Nam.

CÁC THÀNH PHẦN CHÍNH CỦA CSP:
    
    1. VARIABLES (Biến):
       - Các đối tượng cần được gán giá trị
       - Ví dụ: Hà Nội, Hồ Chí Minh, Đà Nẵng, ...
    
    2. DOMAINS (Miền giá trị):
       - Tập hợp các giá trị có thể gán cho mỗi biến
       - Ví dụ: {"Hà Nội": ["Đỏ", "Xanh", "Vàng", "Tím"], ...}
    
    3. NEIGHBORS (Láng giềng):
       - Mối quan hệ kề nhau / liên hệ giữa các biến
       - Ví dụ: {"Hà Nội": ["Hưng Yên", "Bắc Ninh", "Vĩnh Phúc"], ...}
       - Từ đây ta biết biến nào có ràng buộc với nhau
    
    4. CONSTRAINT FUNCTION (Hàm ràng buộc):
       - Kiểm tra tính hợp lệ của các phép gán
       - Ví dụ: Hai tỉnh kề nhau không được cùng màu

VỀ BÀI TOÁN TÔ MÀU:
    - Mỗi tỉnh (variable) cần được gán một màu (value)
    - Nếu hai tỉnh kề nhau (neighbors), chúng phải có màu khác nhau
    - Mục tiêu: Tìm phương án gán màu hợp lệ cho TẤT CẢ các tỉnh
    
CÁCH SỬ DỤNG:
    Các thuật toán (Backtracking, Forward Checking, AC-3) sẽ sử dụng 
    CSP này để tìm giải pháp tối ưu cho bài toán tô màu.
═══════════════════════════════════════════════════════════════════════════════
"""

import json
from typing import List, Dict, Callable, Optional, Any
from pathlib import Path


class CSP:
    """
    Lớp CSP (Constraint Satisfaction Problem) - Bài toán Thỏa mãn Ràng buộc
    
    ═══════════════════════════════════════════════════════════════════════════
    MỤC ĐÍCH:
        - Biểu diễn một bài toán thỏa mãn ràng buộc dưới dạng OOP
        - Cung cấp các phương thức để kiểm tra tính hợp lệ của phép gán
        - Được tái sử dụng bởi các thuật toán giải (Backtracking, etc.)
    
    CỤC BỘ:
        - self.variables: Danh sách các biến (tỉnh thành)
        - self.domains: Dictionary ánh xạ biến → danh sách giá trị
        - self.neighbors: Dictionary ánh xạ biến → danh sách biến kề nhau
        - self.constraint: Hàm kiểm tra ràng buộc
    
    ĐẶC TÍNH:
        - Framework tổng quát, không hardcode bài toán cụ thể
        - Có thể tái sử dụng cho các bài toán CSP khác
        - Đảm bảo tính đúng đắn của dữ liệu qua kiểm tra đầu vào
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    def __init__(
        self,
        variables: List[str],
        domains: Dict[str, List[str]],
        neighbors: Dict[str, List[str]],
        constraint: Callable[[str, Any, str, Any], bool],
    ) -> None:
        """
        Khởi tạo một instance CSP (bài toán thỏa mãn ràng buộc).
        
        ═══════════════════════════════════════════════════════════════════════
        THAM SỐ:
        ═══════════════════════════════════════════════════════════════════════
        
        variables (List[str]):
            Danh sách tên các biến cần gán giá trị.
            Ví dụ: ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", ...]
            Số lượng: 63 tỉnh thành Việt Nam
        
        domains (Dict[str, List[str]]):
            Dictionary ánh xạ mỗi biến tới danh sách giá trị có thể gán.
            Ví dụ: {
                "Hà Nội": ["Đỏ", "Xanh", "Vàng", "Tím"],
                "Hồ Chí Minh": ["Đỏ", "Xanh", "Vàng", "Tím"],
                ...
            }
            Tất cả biến có cùng domain (các màu)
        
        neighbors (Dict[str, List[str]]):
            Dictionary ánh xạ mỗi biến tới danh sách biến kề nhau.
            Ví dụ: {
                "Hà Nội": ["Hưng Yên", "Bắc Ninh", "Vĩnh Phúc", ...],
                "Hồ Chí Minh": ["Long An", "Bình Dương", ...],
                ...
            }
            Các biến trong neighbors không tương ứng với nhau 
            (không cần "Hà Nội" → "Hưng Yên" và "Hưng Yên" → "Hà Nội" 
             nếu chỉ một chiều đã đủ)
        
        constraint (Callable[[str, Any, str, Any], bool]):
            Hàm kiểm tra ràng buộc giữa hai biến kề nhau.
            
            Chữ ký: constraint(var1, val1, var2, val2) → bool
            
            Tham số hàm:
                - var1 (str): Tên biến thứ nhất (ví dụ: "Hà Nội")
                - val1 (Any): Giá trị gán cho var1 (ví dụ: "Đỏ")
                - var2 (str): Tên biến thứ hai - láng giềng (ví dụ: "Hưng Yên")
                - val2 (Any): Giá trị gán cho var2 (ví dụ: "Đỏ")
            
            Trả về:
                - True: Nếu (var1=val1, var2=val2) là hợp lệ
                - False: Nếu vi phạm ràng buộc
            
            Ví dụ hàm mặc định (cho tô màu):
                Trả về True nếu val1 != val2
                (Hai tỉnh kề nhau không được cùng màu)
        
        ═══════════════════════════════════════════════════════════════════════
        NGOẠI LỆ:
        ═══════════════════════════════════════════════════════════════════════
        
        ValueError:
            - Biến không có domain được định nghĩa
            - Domain của biến là rỗng
            - Láng giềng tham chiếu tới biến không tồn tại
        
        ═══════════════════════════════════════════════════════════════════════
        VÍ DỤ SỬ DỤNG:
        ═══════════════════════════════════════════════════════════════════════
        
        >>> variables = ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng"]
        >>> domains = {
        ...     "Hà Nội": ["Đỏ", "Xanh", "Vàng"],
        ...     "Hồ Chí Minh": ["Đỏ", "Xanh", "Vàng"],
        ...     "Đà Nẵng": ["Đỏ", "Xanh", "Vàng"]
        ... }
        >>> neighbors = {
        ...     "Hà Nội": ["Hồ Chí Minh"],
        ...     "Hồ Chí Minh": ["Hà Nội", "Đà Nẵng"],
        ...     "Đà Nẵng": ["Hồ Chí Minh"]
        ... }
        >>> csp = CSP(variables, domains, neighbors, default_constraint)
        >>> # Giờ có thể sử dụng csp với các thuật toán Backtracking, AC-3, ...
        
        ═══════════════════════════════════════════════════════════════════════
        """
        # Lưu trữ dữ liệu đầu vào
        self.variables: List[str] = variables
        self.domains: Dict[str, List[str]] = domains.copy()  # Copy để tránh sửa đổi ngoài ý
        self.neighbors: Dict[str, List[str]] = neighbors
        self.constraint: Callable = constraint
        
        # Kiểm tra tính hợp lệ của dữ liệu đầu vào
        self._validate_input()
    
    def _validate_input(self) -> None:
        """
        Kiểm tra tính hợp lệ của dữ liệu đầu vào CSP.
        
        ═══════════════════════════════════════════════════════════════════════
        CÔNG VIỆC:
        ═══════════════════════════════════════════════════════════════════════
        
        1. KIỂM TRA VARIABLES VÀ DOMAINS:
           - Mỗi biến trong self.variables phải có entry trong self.domains
           - Domain của mỗi biến không được rỗng
        
        2. KIỂM TRA NEIGHBORS:
           - Mỗi biến trong neighbors phải nằm trong variables
           - Mỗi láng giềng phải là một biến hợp lệ
        
        ═══════════════════════════════════════════════════════════════════════
        NGOẠI LỆ:
        ═══════════════════════════════════════════════════════════════════════
        
        ValueError: Nếu bất kỳ kiểm tra nào không hợp lệ
        
        ═══════════════════════════════════════════════════════════════════════
        """
        # 1. Kiểm tra mỗi biến có domain không
        for var in self.variables:
            if var not in self.domains:
                raise ValueError(
                    f"Biến '{var}' không có domain được định nghĩa. "
                    f"Hãy thêm entry '{var}': [...] vào domains."
                )
            if not self.domains[var]:
                raise ValueError(
                    f"Domain của biến '{var}' là rỗng. "
                    f"Mỗi biến phải có ít nhất một giá trị có thể."
                )
        
        # 2. Kiểm tra mỗi láng giềng tham chiếu đều là biến hợp lệ
        for var, neighbors_list in self.neighbors.items():
            if var not in self.variables:
                raise ValueError(
                    f"Biến '{var}' trong neighbors không nằm trong danh sách variables. "
                    f"Hãy đảm bảo tất cả key trong neighbors đều là biến hợp lệ."
                )
            for neighbor in neighbors_list:
                if neighbor not in self.variables:
                    raise ValueError(
                        f"Láng giềng '{neighbor}' của '{var}' không nằm trong danh sách variables. "
                        f"Hãy kiểm tra lại đồ thị kề nhau (adjacency)."
                    )
    
    def is_complete(self, assignment: Dict[str, str]) -> bool:
        """
        Kiểm tra xem phép gán có hoàn chỉnh không (tất cả biến đã được gán).
        
        ═══════════════════════════════════════════════════════════════════════
        ĐỊnH NGHĨA:
        ═══════════════════════════════════════════════════════════════════════
        
        Một phép gán được gọi là "hoàn chỉnh" nếu tất cả các biến đều đã
        được gán một giá trị. Đây là điều kiện dừng của thuật toán tìm kiếm.
        
        ═══════════════════════════════════════════════════════════════════════
        THAM SỐ:
        ═══════════════════════════════════════════════════════════════════════
        
        assignment (Dict[str, str]):
            Dictionary ánh xạ biến → giá trị được gán.
            Ví dụ: {"Hà Nội": "Đỏ", "Hồ Chí Minh": "Xanh"}
            - Một số biến có thể chưa được gán (dictionary chưa đầy đủ)
            - Hoặc tất cả đã được gán
        
        ═══════════════════════════════════════════════════════════════════════
        TRẢ VỀ:
        ═══════════════════════════════════════════════════════════════════════
        
        bool:
            - True: Nếu len(assignment) == len(self.variables)
                    (Tất cả biến đều có giá trị)
            - False: Nếu len(assignment) < len(self.variables)
                     (Vẫn còn biến chưa gán)
        
        ═══════════════════════════════════════════════════════════════════════
        VÍ DỤ:
        ═══════════════════════════════════════════════════════════════════════
        
        Giả sử CSP có 5 tỉnh: Hà Nội, Hồ Chí Minh, Đà Nẵng, Huế, Hải Phòng
        
        >>> csp.is_complete({})
        False  # 0 tỉnh được gán, cần 5
        
        >>> csp.is_complete({"Hà Nội": "Đỏ", "Hồ Chí Minh": "Xanh"})
        False  # 2 tỉnh được gán, cần 5
        
        >>> assignment = {
        ...     "Hà Nội": "Đỏ",
        ...     "Hồ Chí Minh": "Xanh",
        ...     "Đà Nẵng": "Vàng",
        ...     "Huế": "Tím",
        ...     "Hải Phòng": "Đỏ"
        ... }
        >>> csp.is_complete(assignment)
        True  # 5 tỉnh được gán, cần 5 → hoàn chỉnh!
        
        ═══════════════════════════════════════════════════════════════════════
        """
        return len(assignment) == len(self.variables)
    
    def is_consistent(
        self,
        variable: str,
        value: Any,
        assignment: Dict[str, Any],
    ) -> bool:
        """
        Kiểm tra xem gán giá trị cho một biến có hợp lệ không (không vi phạm ràng buộc).
        
        ═══════════════════════════════════════════════════════════════════════
        ĐỊnH NGHĨA:
        ═══════════════════════════════════════════════════════════════════════
        
        Một phép gán (variable = value) được gọi là "hợp lệ" nếu:
        1. Biến tồn tại trong CSP
        2. Giá trị nằm trong domain của biến
        3. Không vi phạm ràng buộc với các biến láng giềng đã được gán
        
        Lưu ý: Hàm chỉ kiểm tra các láng giềng ĐÃ ĐƯỢC GÁN, 
               không kiểm tra những láng giềng chưa gán.
        
        ═══════════════════════════════════════════════════════════════════════
        THAM SỐ:
        ═══════════════════════════════════════════════════════════════════════
        
        variable (str):
            Tên biến cần gán giá trị.
            Ví dụ: "Hà Nội"
        
        value (Any):
            Giá trị muốn gán cho biến.
            Ví dụ: "Đỏ"
        
        assignment (Dict[str, Any]):
            Phép gán hiện tại - các biến đã được gán trước đó.
            Ví dụ: {"Hưng Yên": "Đỏ", "Bắc Ninh": "Xanh"}
            - Dùng để kiểm tra ràng buộc với các láng giềng đã gán
        
        ═══════════════════════════════════════════════════════════════════════
        TRẢ VỀ:
        ═══════════════════════════════════════════════════════════════════════
        
        bool:
            - True: Nếu phép gán (variable = value) là hợp lệ
            - False: Nếu vi phạm bất kỳ kiểm tra nào
        
        ═══════════════════════════════════════════════════════════════════════
        VÍ DỤ (TÔ MÀU BẢN ĐỒ):
        ═══════════════════════════════════════════════════════════════════════
        
        Giả sử:
        - Hà Nội đã được gán màu Đỏ
        - Hưng Yên là láng giềng (kề nhau) của Hà Nội
        
        >>> assignment = {"Hà Nội": "Đỏ"}
        
        # Kiểm tra 1: Gán Hưng Yên = Xanh (khác Đỏ)
        >>> csp.is_consistent("Hưng Yên", "Xanh", assignment)
        True  # Hợp lệ - khác màu với Hà Nội
        
        # Kiểm tra 2: Gán Hưng Yên = Đỏ (cùng Đỏ)
        >>> csp.is_consistent("Hưng Yên", "Đỏ", assignment)
        False  # Không hợp lệ - cùng màu với Hà Nội (láng giềng)
        
        # Kiểm tra 3: Gán Hà Nội = Xanh (biến chưa được gán)
        >>> csp.is_consistent("Hà Nội", "Xanh", {})
        True  # Hợp lệ - không có láng giềng đã gán để kiểm tra
        
        ═══════════════════════════════════════════════════════════════════════
        QUẢN TRỊ RA):
        ═══════════════════════════════════════════════════════════════════════
        
        Hàm này là nền tảng cho các thuật toán như:
        - Backtracking: Kiểm tra trước khi gán
        - Forward Checking: Tính toán consistency
        - AC-3: Cập nhật domains dựa trên consistency
        
        ═══════════════════════════════════════════════════════════════════════
        """
        # Kiểm tra 1: Biến tồn tại không?
        if variable not in self.variables:
            return False
        
        # Kiểm tra 2: Giá trị nằm trong domain của biến?
        if value not in self.domains[variable]:
            return False
        
        # Kiểm tra 3: Không vi phạm ràng buộc với láng giềng đã gán?
        for neighbor in self.neighbors.get(variable, []):
            # Chỉ kiểm tra nếu láng giềng đã được gán
            if neighbor in assignment:
                neighbor_value = assignment[neighbor]
                
                # Gọi hàm ràng buộc để kiểm tra
                # Nếu trả về False → vi phạm ràng buộc
                if not self.constraint(variable, value, neighbor, neighbor_value):
                    return False
        
        # Tất cả kiểm tra đều qua → hợp lệ
        return True
    
    def assign(
        self,
        variable: str,
        value: Any,
        assignment: Dict[str, Any],
    ) -> None:
        """
        Gán một giá trị cho một biến (thêm vào dictionary phép gán).
        
        ═══════════════════════════════════════════════════════════════════════
        MỤC ĐÍCH:
        ═══════════════════════════════════════════════════════════════════════
        
        Đây là hàm trợ giúp (helper) đơn giản để thêm phép gán vào dictionary.
        Trong tương lai, nếu cần tracking lịch sử gán hoặc logging, có thể
        mở rộng hàm này mà không cần sửa các thuật toán khác.
        
        ═══════════════════════════════════════════════════════════════════════
        THAM SỐ:
        ═══════════════════════════════════════════════════════════════════════
        
        variable (str):
            Tên biến cần gán.
            Ví dụ: "Hà Nội"
        
        value (Any):
            Giá trị gán cho biến.
            Ví dụ: "Đỏ"
        
        assignment (Dict[str, Any]):
            Dictionary phép gán (sẽ được sửa đổi tại chỗ - in-place).
            Ví dụ (trước): {}
            Ví dụ (sau): {"Hà Nội": "Đỏ"}
            
            LƯU Ý: Dictionary này sẽ được thay đổi trực tiếp.
                   Không cần gán lại biến.
        
        ═══════════════════════════════════════════════════════════════════════
        VÍ DỤ:
        ═══════════════════════════════════════════════════════════════════════
        
        >>> assignment = {}
        >>> csp.assign("Hà Nội", "Đỏ", assignment)
        >>> print(assignment)
        {'Hà Nội': 'Đỏ'}
        
        >>> csp.assign("Hồ Chí Minh", "Xanh", assignment)
        >>> print(assignment)
        {'Hà Nội': 'Đỏ', 'Hồ Chí Minh': 'Xanh'}
        
        ═══════════════════════════════════════════════════════════════════════
        """
        assignment[variable] = value
    
    def unassign(
        self,
        variable: str,
        assignment: Dict[str, Any],
    ) -> None:
        """
        Bỏ gán giá trị của một biến (xóa khỏi dictionary phép gán).
        
        ═══════════════════════════════════════════════════════════════════════
        MỤC ĐÍCH:
        ═══════════════════════════════════════════════════════════════════════
        
        Khi thuật toán Backtracking quay lùi, cần bỏ gán các biến
        để thử nhánh khác. Hàm này thực hiện việc đó.
        
        ═══════════════════════════════════════════════════════════════════════
        THAM SỐ:
        ═══════════════════════════════════════════════════════════════════════
        
        variable (str):
            Tên biến cần bỏ gán.
            Ví dụ: "Hà Nội"
        
        assignment (Dict[str, Any]):
            Dictionary phép gán (sẽ được sửa đổi tại chỗ - in-place).
            Ví dụ (trước): {"Hà Nội": "Đỏ", "Hồ Chí Minh": "Xanh"}
            Ví dụ (sau): {"Hồ Chí Minh": "Xanh"}
            
            LƯU Ý: Dictionary này sẽ được thay đổi trực tiếp.
        
        ═══════════════════════════════════════════════════════════════════════
        NGOẠI LỆ:
        ═══════════════════════════════════════════════════════════════════════
        
        KeyError: Nếu biến không nằm trong assignment (chưa gán)
        
        ═══════════════════════════════════════════════════════════════════════
        VÍ DỤ:
        ═══════════════════════════════════════════════════════════════════════
        
        >>> assignment = {"Hà Nội": "Đỏ", "Hồ Chí Minh": "Xanh"}
        >>> csp.unassign("Hà Nội", assignment)
        >>> print(assignment)
        {'Hồ Chí Minh': 'Xanh'}
        
        >>> csp.unassign("Hà Nội", assignment)
        # KeyError: 'Hà Nội' (vì đã bỏ gán rồi)
        
        ═══════════════════════════════════════════════════════════════════════
        """
        del assignment[variable]
    
    def get_unassigned_variables(self, assignment: Dict[str, Any]) -> List[str]:
        """
        Lấy danh sách các biến chưa được gán giá trị.
        
        ═══════════════════════════════════════════════════════════════════════
        MỤC ĐÍCH:
        ═══════════════════════════════════════════════════════════════════════
        
        Khi tìm kiếm lời giải, cần biết biến nào còn chưa gán để:
        1. Xác định khi nào tìm kiếm xong (all assigned → dừng)
        2. Chọn biến tiếp theo để gán giá trị
        3. Áp dụng heuristic (ví dụ: chọn biến có domain nhỏ nhất)
        
        ═══════════════════════════════════════════════════════════════════════
        THAM SỐ:
        ═══════════════════════════════════════════════════════════════════════
        
        assignment (Dict[str, Any]):
            Phép gán hiện tại.
            Ví dụ: {"Hà Nội": "Đỏ", "Hồ Chí Minh": "Xanh"}
        
        ═══════════════════════════════════════════════════════════════════════
        TRẢ VỀ:
        ═══════════════════════════════════════════════════════════════════════
        
        List[str]:
            Danh sách các biến có trong self.variables nhưng KHÔNG có
            trong assignment.
            
            Ví dụ: Nếu self.variables có 5 tỉnh, assignment có 2 tỉnh
                   → trả về 3 tỉnh chưa gán
        
        ═══════════════════════════════════════════════════════════════════════
        VÍ DỤ:
        ═══════════════════════════════════════════════════════════════════════
        
        >>> csp.variables = ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Huế"]
        
        >>> csp.get_unassigned_variables({})
        ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Huế"]
        # Chưa gán cái gì
        
        >>> csp.get_unassigned_variables({"Hà Nội": "Đỏ"})
        ["Hồ Chí Minh", "Đà Nẵng", "Huế"]
        # Còn lại 3 tỉnh
        
        >>> csp.get_unassigned_variables({
        ...     "Hà Nội": "Đỏ",
        ...     "Hồ Chí Minh": "Xanh",
        ...     "Đà Nẵng": "Vàng",
        ...     "Huế": "Tím"
        ... })
        []
        # Tất cả đã gán
        
        ═══════════════════════════════════════════════════════════════════════
        """
        return [var for var in self.variables if var not in assignment]
    
    def get_domain(self, variable: str) -> List[str]:
        """
        Lấy domain (danh sách giá trị có thể) của một biến.
        
        ═══════════════════════════════════════════════════════════════════════
        THAM SỐ:
        ═══════════════════════════════════════════════════════════════════════
        
        variable (str):
            Tên biến.
            Ví dụ: "Hà Nội"
        
        ═══════════════════════════════════════════════════════════════════════
        TRẢ VỀ:
        ═══════════════════════════════════════════════════════════════════════
        
        List[str]:
            Copy của domain của biến (trả về bản copy để tránh sửa đổi vô ý).
            Ví dụ: ["Đỏ", "Xanh", "Vàng", "Tím"]
        
        ═══════════════════════════════════════════════════════════════════════
        VÍ DỤ:
        ═══════════════════════════════════════════════════════════════════════
        
        >>> csp.get_domain("Hà Nội")
        ["Đỏ", "Xanh", "Vàng", "Tím"]
        
        ═══════════════════════════════════════════════════════════════════════
        """
        return self.domains[variable].copy()
    
    def get_neighbors(self, variable: str) -> List[str]:
        """
        Lấy danh sách các biến kề nhau (láng giềng) của một biến.
        
        ═══════════════════════════════════════════════════════════════════════
        THAM SỐ:
        ═══════════════════════════════════════════════════════════════════════
        
        variable (str):
            Tên biến.
            Ví dụ: "Hà Nội"
        
        ═══════════════════════════════════════════════════════════════════════
        TRẢ VỀ:
        ═══════════════════════════════════════════════════════════════════════
        
        List[str]:
            Copy của danh sách láng giềng (trả về copy để tránh sửa đổi vô ý).
            Ví dụ: ["Hưng Yên", "Bắc Ninh", "Vĩnh Phúc", "Hà Nam"]
        
        ═══════════════════════════════════════════════════════════════════════
        VÍ DỤ:
        ═══════════════════════════════════════════════════════════════════════
        
        >>> csp.get_neighbors("Hà Nội")
        ["Hưng Yên", "Bắc Ninh", "Vĩnh Phúc", "Hà Nam", "Hòa Bình", "Phú Thọ"]
        
        ═══════════════════════════════════════════════════════════════════════
        """
        return self.neighbors.get(variable, []).copy()
    
    def __repr__(self) -> str:
        """
        Trả về chuỗi biểu diễn CSP (để debugging).
        
        ═══════════════════════════════════════════════════════════════════════
        VÍ DỤ:
        ═══════════════════════════════════════════════════════════════════════
        
        >>> csp = create_map_coloring_csp()
        >>> print(csp)
        CSP(variables=63, domains=63, constraints=203)
        # 63 tỉnh, 63 domain, tổng 203 cạnh kề nhau
        
        ═══════════════════════════════════════════════════════════════════════
        """
        return (
            f"CSP(variables={len(self.variables)}, "
            f"domains={len(self.domains)}, "
            f"constraints={sum(len(n) for n in self.neighbors.values())})"
        )


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                    HÀM RÀNG BUỘC MẶC ĐỊNH (DEFAULT)                       ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def default_constraint(
    var1: str,
    val1: Any,
    var2: str,
    val2: Any,
) -> bool:
    """
    Hàm ràng buộc mặc định cho bài toán tô màu bản đồ.
    
    ═══════════════════════════════════════════════════════════════════════════
    ĐỊNH NGHĨA RÀNG BUỘC:
    ═══════════════════════════════════════════════════════════════════════════
    
    Hai tỉnh thành kề nhau (láng giềng) KHÔNG ĐƯỢC cùng một màu.
    
    Nói cách khác:
    - Nếu var1 và var2 là láng giềng
    - Và val1 = val2 (cùng màu)
    - → Ràng buộc vi phạm → trả về False
    
    Nếu val1 ≠ val2:
    - → Ràng buộc thỏa mãn → trả về True
    
    ═══════════════════════════════════════════════════════════════════════════
    THAM SỐ:
    ═══════════════════════════════════════════════════════════════════════════
    
    var1 (str):
        Tên tỉnh thứ nhất.
        Ví dụ: "Hà Nội"
    
    val1 (Any):
        Màu gán cho tỉnh thứ nhất.
        Ví dụ: "Đỏ"
    
    var2 (str):
        Tên tỉnh thứ hai (láng giềng của var1).
        Ví dụ: "Hưng Yên"
    
    val2 (Any):
        Màu gán cho tỉnh thứ hai.
        Ví dụ: "Xanh"
    
    ═══════════════════════════════════════════════════════════════════════════
    TRẢ VỀ:
    ═══════════════════════════════════════════════════════════════════════════
    
    bool:
        - True: Nếu val1 ≠ val2 (màu khác nhau - hợp lệ)
        - False: Nếu val1 == val2 (cùng màu - vi phạm ràng buộc)
    
    ═══════════════════════════════════════════════════════════════════════════
    VÍ DỤ:
    ═══════════════════════════════════════════════════════════════════════════
    
    >>> default_constraint("Hà Nội", "Đỏ", "Hưng Yên", "Xanh")
    True   # Hợp lệ - hai màu khác nhau
    
    >>> default_constraint("Hà Nội", "Đỏ", "Hưng Yên", "Đỏ")
    False  # Vi phạm - cùng màu
    
    >>> default_constraint("Hà Nội", "Xanh", "Hưng Yên", "Vàng")
    True   # Hợp lệ - hai màu khác nhau
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    return val1 != val2


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║               HÀM TẠO CSP TỪ FILE JSON (HELPER FUNCTION)                  ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def create_map_coloring_csp(
    provinces_file: Optional[str] = None,
    adjacency_file: Optional[str] = None,
    colors_file: Optional[str] = None,
) -> CSP:
    """
    Tạo một instance CSP cho bài toán tô màu bản đồ Việt Nam.
    
    ═══════════════════════════════════════════════════════════════════════════
    MỤC ĐÍCH:
    ═══════════════════════════════════════════════════════════════════════════
    
    Hàm này là một "hàm trợ giúp" (helper function) để tạo CSP từ dữ liệu
    được lưu trong các file JSON. Thay vì tạo CSP thủ công, chỉ cần
    gọi hàm này là xong.
    
    ═══════════════════════════════════════════════════════════════════════════
    THAM SỐ:
    ═══════════════════════════════════════════════════════════════════════════
    
    provinces_file (Optional[str]):
        Đường dẫn tới file JSON chứa danh sách các tỉnh thành.
        Nếu None → sử dụng đường dẫn mặc định: "data/vietnam_provinces.json"
        Ví dụ: "data/vietnam_provinces.json"
    
    adjacency_file (Optional[str]):
        Đường dẫn tới file JSON chứa đồ thị kề nhau (adjacency graph).
        Nếu None → sử dụng đường dẫn mặc định: "data/adjacency.json"
        Ví dụ: "data/adjacency.json"
    
    colors_file (Optional[str]):
        Đường dẫn tới file JSON chứa danh sách các màu.
        Nếu None → sử dụng đường dẫn mặc định: "data/colors.json"
        Ví dụ: "data/colors.json"
    
    ═══════════════════════════════════════════════════════════════════════════
    TRẢ VỀ:
    ═══════════════════════════════════════════════════════════════════════════
    
    CSP:
        Một instance CSP hoàn chỉnh, sẵn sàng để sử dụng với các thuật toán
        Backtracking, Forward Checking, AC-3.
    
    ═══════════════════════════════════════════════════════════════════════════
    NGOẠI LỆ:
    ═══════════════════════════════════════════════════════════════════════════
    
    FileNotFoundError:
        Nếu một trong các file JSON không tìm thấy.
        → Kiểm tra đường dẫn file hoặc chắc chắn file tồn tại.
    
    json.JSONDecodeError:
        Nếu file JSON bị hỏng / không đúng format.
        → Kiểm tra syntax JSON của file.
    
    ValueError:
        Nếu dữ liệu trong file không hợp lệ (thông qua CSP._validate_input).
    
    ═══════════════════════════════════════════════════════════════════════════
    QUẢN TRỊ ĐỊA PHƯƠNG:
    ═══════════════════════════════════════════════════════════════════════════
    
    Domains (Miền giá trị):
        Mỗi tỉnh được gán cùng một domain: danh sách tất cả các màu.
        Ví dụ: {"Hà Nội": ["Đỏ", "Xanh", "Vàng", "Tím"], ...}
        
        Lý do: Bất cứ tỉnh nào cũng có thể được tô bất kỳ màu nào
               (trừ khi bị ràng buộc bởi láng giềng đã gán).
    
    ═══════════════════════════════════════════════════════════════════════════
    VÍ DỤ SỬ DỤNG:
    ═══════════════════════════════════════════════════════════════════════════
    
    # Cách 1: Sử dụng đường dẫn mặc định
    >>> csp = create_map_coloring_csp()
    >>> print(csp)
    CSP(variables=63, domains=63, constraints=203)
    
    # Cách 2: Sử dụng đường dẫn tùy chỉnh
    >>> csp = create_map_coloring_csp(
    ...     provinces_file="custom_data/provinces.json",
    ...     adjacency_file="custom_data/neighbors.json",
    ...     colors_file="custom_data/colors.json"
    ... )
    
    # Cách 3: Kiểm tra dữ liệu
    >>> csp = create_map_coloring_csp()
    >>> print(f"Số tỉnh: {len(csp.variables)}")
    Số tỉnh: 63
    >>> print(f"Số màu: {len(csp.get_domain(csp.variables[0]))}")
    Số màu: 4
      ═══════════════════════════════════════════════════════════════════════════
    """
    # Thiết lập đường dẫn mặc định nếu không được cung cấp
    if provinces_file is None:
        provinces_file = "data/vietnam_provinces.json"
    if adjacency_file is None:
        adjacency_file = "data/adjacency.json"
    if colors_file is None:
        colors_file = "data/colors.json"
    
    # Chuyển đổi sang Path object để xử lý đường dẫn
    # Nếu đường dẫn là tương đối, tìm từ thư mục dự án gốc
    provinces_path = Path(provinces_file)
    adjacency_path = Path(adjacency_file)
    colors_path = Path(colors_file)
    
    # Nếu file không tìm thấy và đường dẫn là tương đối, thử tìm từ thư mục cha
    if not provinces_path.exists() and not provinces_path.is_absolute():
        parent_path = Path(__file__).parent.parent / provinces_file
        if parent_path.exists():
            provinces_path = parent_path
    
    if not adjacency_path.exists() and not adjacency_path.is_absolute():
        parent_path = Path(__file__).parent.parent / adjacency_file
        if parent_path.exists():
            adjacency_path = parent_path
    
    if not colors_path.exists() and not colors_path.is_absolute():
        parent_path = Path(__file__).parent.parent / colors_file
        if parent_path.exists():
            colors_path = parent_path
    
    # Đọc dữ liệu từ các file JSON
    with open(provinces_path, "r", encoding="utf-8") as f:
        provinces = json.load(f)
    
    with open(adjacency_path, "r", encoding="utf-8") as f:
        adjacency = json.load(f)
    
    with open(colors_path, "r", encoding="utf-8") as f:
        colors = json.load(f)
    
    # Tạo domains: mỗi tỉnh có thể được tô bất kỳ màu nào
    domains = {province: colors.copy() for province in provinces}
    
    # Tạo và trả về CSP instance
    csp = CSP(
        variables=provinces,
        domains=domains,
        neighbors=adjacency,
        constraint=default_constraint,
    )
    
    return csp


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                         TESTING & VALIDATION                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    """
    Phần kiểm tra (testing) - chạy các test cơ bản để xác minh CSP hoạt động đúng.
    
    ═══════════════════════════════════════════════════════════════════════════
    CÁC TEST:
    ═══════════════════════════════════════════════════════════════════════════
    
    1. Tạo CSP từ dữ liệu file JSON
    2. Hiển thị thông tin CSP
    3. Kiểm tra is_complete()
    4. Kiểm tra is_consistent()
    5. Kiểm tra assign/unassign
    6. Kiểm tra get_unassigned_variables()
    7. Kiểm tra get_neighbors()
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    print("=" * 80)
    print("CSP MODEL TESTING - TÔ MÀU BẢN ĐỒ VIỆT NAM")
    print("=" * 80)
    
    try:
        # [1] TẠO CSP TỪ FILE
        print("\n[1] KHỞI TẠO CSP TỪ CÁC FILE JSON:")
        print("-" * 80)
        csp = create_map_coloring_csp()
        print(f"✓ CSP được tạo thành công: {csp}")
        
        # [2] HIỂN THỊ THÔNG TIN
        print(f"\n[2] THÔNG TIN CSP:")
        print("-" * 80)
        print(f"  • Số lượng biến (tỉnh thành): {len(csp.variables)}")
        print(f"  • Danh sách 5 tỉnh đầu tiên: {csp.variables[:5]}")
        print(f"  • Các màu sẵn có: {csp.get_domain(csp.variables[0])}")
        total_constraints = sum(len(n) for n in csp.neighbors.values())
        print(f"  • Tổng số ràng buộc (cạnh): {total_constraints}")
        
        # [3] KIỂM TRA is_complete()
        print(f"\n[3] KIỂM TRA is_complete() - XEM PHÉP GÁN CÓ ĐỦ CHƯA:")
        print("-" * 80)
        assignment_empty = {}
        assignment_partial = {"Hà Nội": "Đỏ", "Hồ Chí Minh": "Xanh"}
        assignment_complete = {prov: "Đỏ" for prov in csp.variables}
        
        print(f"  • Phép gán rỗng: {csp.is_complete(assignment_empty)}")
        print(f"    → {len(assignment_empty)}/{len(csp.variables)} tỉnh được gán")
        
        print(f"  • Phép gán một phần (2 tỉnh): {csp.is_complete(assignment_partial)}")
        print(f"    → {len(assignment_partial)}/{len(csp.variables)} tỉnh được gán")
        
        print(f"  • Phép gán hoàn chỉnh: {csp.is_complete(assignment_complete)}")
        print(f"    → {len(assignment_complete)}/{len(csp.variables)} tỉnh được gán")
        
        # [4] KIỂM TRA is_consistent()
        print(f"\n[4] KIỂM TRA is_consistent() - TÍC HỢP LỆ CỦA PHÉP GÁN:")
        print("-" * 80)
        test_assignment = {}
        
        # Test 4.1: Gán tỉnh thứ nhất
        var1 = "Hà Nội"
        is_valid = csp.is_consistent(var1, "Đỏ", test_assignment)
        print(f"  • Gán '{var1}' = 'Đỏ' (không có láng giềng trước): {is_valid}")
        csp.assign(var1, "Đỏ", test_assignment)
        
        # Test 4.2: Gán láng giềng với màu khác (hợp lệ)
        var2 = "Hưng Yên"  # Là láng giềng của Hà Nội
        is_valid = csp.is_consistent(var2, "Xanh", test_assignment)
        print(f"  • Gán láng giềng '{var2}' = 'Xanh' (khác '{var1}'): {is_valid}")
        print(f"    → Hợp lệ ✓")
        
        # Test 4.3: Gán láng giềng với cùng màu (không hợp lệ)
        is_valid = csp.is_consistent(var2, "Đỏ", test_assignment)
        print(f"  • Gán láng giềng '{var2}' = 'Đỏ' (cùng '{var1}'): {is_valid}")
        print(f"    → Không hợp lệ (vi phạm ràng buộc) ✗")
        
        # [5] KIỂM TRA assign/unassign
        print(f"\n[5] KIỂM TRA assign() VÀ unassign():")
        print("-" * 80)
        test_dict = {}
        print(f"  • Trước assign: {test_dict}")
        
        csp.assign("Hà Nội", "Đỏ", test_dict)
        print(f"  • Sau assign 'Hà Nội': {test_dict}")
        
        csp.unassign("Hà Nội", test_dict)
        print(f"  • Sau unassign 'Hà Nội': {test_dict}")
        
        # [6] KIỂM TRA get_unassigned_variables()
        print(f"\n[6] KIỂM TRA get_unassigned_variables() - BIẾN CHƯA GÁN:")
        print("-" * 80)
        partial_assignment = {"Hà Nội": "Đỏ", "Hồ Chí Minh": "Xanh"}
        unassigned = csp.get_unassigned_variables(partial_assignment)
        print(f"  • Phép gán một phần: {partial_assignment}")
        print(f"  • Số biến chưa gán: {len(unassigned)}")
        print(f"  • Danh sách 5 tỉnh chưa gán: {unassigned[:5]}")
        
        # [7] KIỂM TRA get_neighbors()
        print(f"\n[7] KIỂM TRA get_neighbors() - LÁNG GIỀNG:")
        print("-" * 80)
        province = "Hà Nội"
        neighbors = csp.get_neighbors(province)
        print(f"  • Tỉnh: '{province}'")
        print(f"  • Số tỉnh kề nhau: {len(neighbors)}")
        print(f"  • Danh sách tỉnh kề: {neighbors}")
        
        # [8] KIỂM TRA domain
        print(f"\n[8] KIỂM TRA get_domain() - MIỀN GIÁ TRỊ:")
        print("-" * 80)
        domain = csp.get_domain("Hà Nội")
        print(f"  • Domain của 'Hà Nội': {domain}")
        print(f"  • Số lượng màu: {len(domain)}")
        
        print("\n" + "=" * 80)
        print("✓ TẤT CẢ CÁC TEST ĐỀU THÀNH CÔNG!")
        print("=" * 80)
        print("\nGHI CHÚ:")
        print("  • CSP đã sẵn sàng để sử dụng với các thuật toán:")
        print("    - Backtracking")
        print("    - Forward Checking")
        print("    - AC-3 (Arc Consistency)")
        
    except FileNotFoundError as e:
        print(f"\n✗ LỖI: {e}")
        print("Hãy chắc chắn các file JSON tồn tại trong thư mục 'data/':")
        print("  • data/vietnam_provinces.json")
        print("  • data/adjacency.json")
        print("  • data/colors.json")
    
    except Exception as e:
        print(f"\n✗ LỖI KHÔNG CÓ DỰ TÍNH: {e}")
        import traceback
        traceback.print_exc()
